from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from shop.models import Product, UserProductRelation


class ProductSerializer(ModelSerializer):
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'seller', 'rating')


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserProductRelationSerializer(ModelSerializer):
    class Meta:
        model = UserProductRelation
        fields = ('product', 'favourites', 'rate')
