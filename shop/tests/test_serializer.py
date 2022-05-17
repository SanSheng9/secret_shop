from django.contrib.auth.models import User
from django.test import TestCase

from shop.models import Product, UserProductRelation
from shop.serializers import ProductSerializer


class ProductSerializerTestCase(TestCase):
    def test_ok(self):
        user_1 = User.objects.create(username='user1')
        user_2 = User.objects.create(username='user2')


        product_1 = Product.objects.create(name='Test product 1', price='100', seller=user_1)
        product_2 = Product.objects.create(name='Test product 2', price='150', seller=user_1)
        product_3 = Product.objects.create(name='Test product 3', price='40', seller=user_2)
        UserProductRelation.objects.create(user=user_1, product=product_1, favourites=True, rate=5)
        UserProductRelation.objects.create(user=user_1, product=product_2, favourites=True, rate=1)
        UserProductRelation.objects.create(user=user_1, product=product_3, favourites=True, rate=3)
        UserProductRelation.objects.create(user=user_2, product=product_1, favourites=True, rate=1)
        UserProductRelation.objects.create(user=user_2, product=product_2, favourites=True, rate=4)
        UserProductRelation.objects.create(user=user_2, product=product_3, favourites=True, rate=5)

        data = ProductSerializer([product_1, product_2, product_3], many=True).data
        expected_data = [
            {
                'id': product_1.id,
                'name': 'Test product 1',
                'price': '100.00',
                'seller': product_1.seller.id,
                'rating': '3.00'
            },
            {
                'id': product_2.id,
                'name': 'Test product 2',
                'price': '150.00',
                'seller': product_2.seller.id,
                'rating': '2.50'
            },
            {
                'id': product_3.id,
                'name': 'Test product 3',
                'price': '40.00',
                'seller': product_3.seller.id,
                'rating': '4.00'
            },
        ]
        self.assertEqual(expected_data, data)