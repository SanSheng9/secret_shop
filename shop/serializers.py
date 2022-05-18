from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from shop.models import Product, UserProductRelation


class ProductSerializer(ModelSerializer):
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
#    favourites = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'img', 'price', 'seller', 'rating')

    #def get_favourites(self, instance, request):
    #    obj = UserProductRelation.objects.values('favourites').filter(pk=instance.id, user=request.user)
    #    return obj

class UserSerializer(ModelSerializer):
    favourites = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar', 'is_superuser', 'favourites')

    def get_favourites(self, instance):
        return UserProductRelation.objects.values_list('product', flat=True).filter(user=instance.id, favourites=True)

class UserProductRelationSerializer(ModelSerializer):
    class Meta:
        model = UserProductRelation
        fields = ('product', 'favourites', 'rate')
