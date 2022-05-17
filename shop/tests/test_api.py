import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from shop.models import Product, UserProductRelation
from shop.serializers import ProductSerializer


class ProductApiTestCase(APITestCase):
    def setUp(self):
        self.product_1 = Product.objects.create(name='Test product 1', price='100', count='2')
        self.product_2 = Product.objects.create(name='Test product 2', price='150', count='4')
        self.user = User.objects.create(username='test_user')
        UserProductRelation.objects.create(user=self.user, product=self.product_1, favourites=True, rate=5)

    def test_get(self):
        url = reverse('product-list')
        response = self.client.get(url)
        serializer_data = ProductSerializer([self.product_1, self.product_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('product-list')
        response = self.client.get(url, data={'price': 100})
        serializer_data = ProductSerializer([self.product_1], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(2, Product.objects.all().count())
        url = reverse('product-list')
        self.client.force_login(self.user)
        data = json.dumps({
            "name": "Product test",
            "price": "100.00",
        })
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Product.objects.all().count())
        self.assertEqual(self.user, Product.objects.last().seller)
