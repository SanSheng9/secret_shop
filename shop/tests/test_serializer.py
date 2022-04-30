from django.test import TestCase

from shop.models import Product
from shop.serializers import ProductSerializer


class ProductSerializerTestCase(TestCase):
    def setUp(self):
        self.product_1 = Product.objects.create(name='Test product 1', price='100')
        self.product_2 = Product.objects.create(name='Test product 2', price='150')

    def test_ok(self):

        data = ProductSerializer([self.product_1, self.product_2], many=True).data
        expected_data = [
            {
                'id': self.product_1.id,
                'name': 'Test product 1',
                'price': '100.00',
            },
            {
                'id': self.product_2.id,
                'name': 'Test product 2',
                'price': '150.00',
            }
        ]
        self.assertEqual(expected_data, data)