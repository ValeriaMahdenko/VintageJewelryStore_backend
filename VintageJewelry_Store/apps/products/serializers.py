from rest_framework import serializers
from .models import Product, ProductImage
from rest_framework.exceptions import NotAcceptable
from django.forms import ImageField as DjangoImageField


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['product', 'image']
        extra_kwargs = {
            'product': {'required': False}
        }

    def validate(self, attrs):
        default_error_messages = {
            'invalid_image':
                'The file you uploaded was either not an image or invalid one.'
        }
        for i in self.initial_data.getlist('image'):
            django_field = DjangoImageField()
            django_field.error_messages = default_error_messages
            django_field.clean(i)
        return attrs


class ProductGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    images = ProductImageSerializer(allow_null=True, many=True, required=False)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    images = ProductImageSerializer(allow_null=True, many=True, required=False)

    def create(self, validated_data):
        try:
            product_obj = super(ProductSerializer, self).create(validated_data)
        except Exception:
            raise NotAcceptable(
                detail={'message': 'The request is not acceptable.'}, code=406)

        if 'included_images' in self.context:
            images_data = self.context['included_images']
            for i in images_data.getlist('image'):
                ProductImage.objects.create(
                    product=product_obj,
                    image=i
                )
        return product_obj

    def update(self, instance, validated_data):
        if 'included_images' in self.context:
            images_data = self.context['included_images']
            ProductImage.objects.filter(product=instance).delete()
            for i in images_data.getlist('image'):
                ProductImage.objects.create(
                    product=instance,
                    image=i
                )
        return super().update(instance, validated_data)
