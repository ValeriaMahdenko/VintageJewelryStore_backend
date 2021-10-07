from rest_framework import serializers
from .models import Product
from rest_framework.exceptions import NotAcceptable


class ProductGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        try:
            product_obj = super(ProductSerializer, self).create(validated_data)
        except Exception:
            raise NotAcceptable(
                detail={'message': 'The request is not acceptable.'}, code=406)

        return product_obj
