from rest_framework import serializers
from django_countries import Countries
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model

User = get_user_model()


class SerializableCountryField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        super(SerializableCountryField, self).__init__(choices=Countries(),
         allow_blank=True, required=False)

    def to_representation(self, value):
        if value in ('', None):
            return ''
        return super(SerializableCountryField, self).to_representation(value)


class SuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        permission_classes = [IsAdminUser]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    country = SerializableCountryField()

    class Meta:
        model = User
        exclude = ['is_admin', 'is_superuser', 'is_active', 'last_login']

    def create(self, validated_data):
        validated_data['password'] = make_password(
            validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
