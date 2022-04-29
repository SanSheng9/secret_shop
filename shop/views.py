from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from shop.models import Product
from shop.serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

