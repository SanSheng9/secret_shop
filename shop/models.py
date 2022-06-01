from django.contrib.auth.models import AbstractUser
from django.db import models

from secret_shop import settings


class UserProfile(AbstractUser):
    email = models.CharField(max_length=100, unique=True)
    username = models.CharField(primary_key=True, max_length=100, unique=True)
    password = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='photos/%Y/%m/%d', blank=False, default='avatar.svg', verbose_name='Аватар')
    about_me = models.CharField(max_length=255, default="I'm new user!", blank=False)


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    img = models.ImageField(upload_to='photos/%Y/%m/%d', blank=False, default='default.svg')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='my_products')
    shoppers = models.ManyToManyField(settings.AUTH_USER_MODEL, through='UserProductRelation', related_name='products')
    count = models.PositiveSmallIntegerField(blank=False, default=1)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, default=None, null=True)

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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    favourites = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)
    bucket = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}: {self.product}, RATE: {self.rate}'

    def __init__(self, *args, **kwargs):
        super(UserProductRelation, self).__init__(*args, **kwargs)
        self.old_rate = self.rate

    def save(self, *args, **kwargs):
        creating = not self.pk

        super().save(*args, **kwargs)

        if self.old_rate != self.rate or creating:
            from shop.logic import set_rating
            set_rating(self.product)
