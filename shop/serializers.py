from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from shop.models import Product, UserProductRelation, UserProfile


class ProductSerializer(ModelSerializer):
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)

    #    favourites = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'img', 'price', 'seller', 'rating')

    # def get_favourites(self, instance, request):
    #    obj = UserProductRelation.objects.values('favourites').filter(pk=instance.id, user=request.user)
    #    return obj


class UserSerializer(ModelSerializer):
    favourites = serializers.SerializerMethodField(read_only=True)
    bucket = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('username', 'avatar', 'is_superuser',
                  'favourites', 'bucket')

    def get_favourites(self, instance):
        return UserProductRelation.objects.values_list('product', flat=True).filter(user=instance.username,
                                                                                        favourites=True)

    def get_bucket(self, instance):
        return UserProductRelation.objects.values_list('product', flat=True).filter(user=instance.username,
                                                                                        bucket=True)


class UserProductRelationSerializer(ModelSerializer):
    class Meta:
        model = UserProductRelation
        fields = ('product', 'favourites', 'rate')
