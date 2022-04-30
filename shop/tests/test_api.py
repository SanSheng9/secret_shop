import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from shop.models import Product
from shop.serializers import ProductSerializer


class ProductApiTestCase(APITestCase):
    profile_list_url = reverse('all-profiles')

    def setUp(self):
        self.product_1 = Product.objects.create(name='Test product 1', price='100')
        self.product_2 = Product.objects.create(name='Test product 2', price='150')
        data = json.dumps({
            "username": "testuser",
            "password": "oral1234"
        })
        self.user = self.client.post("/auth/users/", data, content_type="application/json")
        response = self.client.post("/auth/jwt/create/", data, content_type="application/json")
        self.token = response.data["access"]
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

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
        url = reverse('product-list')
        data = json.dumps({
            "name": "Product test",
            "price": "100.00"
        })
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
