from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from shop.models import Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
