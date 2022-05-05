from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='my_products')
    shoppers = models.ManyToManyField(User, through='UserProductRelation', related_name='products')
    count = models.PositiveSmallIntegerField(blank=False)

    def __str__(self):
        return f'ID {self.id}: {self.name}'


class UserProductRelation(models.Model):
    RATE_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    favourites = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return f'{self.user.username}: {self.product}, RATE: {self.rate}'
