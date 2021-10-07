from VintageJewelry_Store.apps.products.models import Product
from rest_framework import serializers
from .models import Order, OrderProducts
from VintageJewelry_Store.apps.users.serializers import UserSerializer


class OrderProductsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProducts
        fields = ['order', 'amount_selected', 'product']
        read_only_fields = ['order']


class OrderProductsGetSerializer(serializers.ModelSerializer):
    product = serializers.ReadOnlyField(source='product.id')

    class Meta:
        model = OrderProducts
        fields = ['product', 'amount_selected']


class OrderGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['total_price', 'customer', 'selected_products']

    selected_products = OrderProductsGetSerializer(
        source='orderproducts_set', many=True)
    customer = UserSerializer()
    total_price = serializers.SerializerMethodField(
        method_name='get_total_price')

    def get_total_price(self, instance):
        if instance.total_price is None:
            return None
        return "%.2f" % round(instance.total_price, 2)


class OrderPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['total_price', 'customer']

    selected_products = OrderProductsPostSerializer(
        source='orderproducts_set', many=True)

    def create(self, validated_data):
        total_price = 0
        products_list = validated_data.pop('orderproducts_set')
        order = Order.objects.create(**validated_data)
        for product_dict in products_list:
            product = product_dict['product']
            amount_selected = product_dict['amount_selected']
            if amount_selected <= product.amount:
                OrderProducts.objects.create(amount_selected=amount_selected,
                    product=product, order=order)
                total_price += product.price * amount_selected
                product.amount -= amount_selected
                product.save()
            else:
                order.delete()
                raise serializers.ValidationError(
                    'Not enough units of this product available')
        # delete order with no selected products
        if total_price == 0:
            order.delete()
            raise serializers.ValidationError(
                'Please add products to the order')
        order.total_price = total_price
        order.save()
        return order

    def update(self, order, validated_data):
        if 'orderproducts_set' in validated_data:
            products_list = validated_data.pop('orderproducts_set')
            # Restore back available amount of removed products in db
            old_order_products = OrderProducts.objects.filter(order=order.id)
            for old_order_product in old_order_products:
                product = Product.objects.get(pk=old_order_product.product.pk)
                product.amount += old_order_product.amount_selected
                product.save()
                old_order_product.delete()
            total_price = 0
            # Decrease available amount of selected products i db
            # and calculate total price
            for product_dict in products_list:
                product = product_dict['product']
                amount_selected = product_dict['amount_selected']
                if amount_selected <= product.amount:
                    OrderProducts.objects.create(
                        amount_selected=amount_selected, product=product,
                        order=order)
                    total_price += product.price * amount_selected
                    product.amount -= amount_selected
                    product.save()
                else:
                    order.delete()
                    raise serializers.ValidationError(
                        'Not enough units of this product')
            order.total_price = total_price
            # delete order with no selected products
            if total_price == 0:
                order.delete()
                raise serializers.ValidationError(
                    'Please add products to the order')
        for key, value in validated_data.items():
            setattr(order, key, value)
        order.save()
        return order
