from django.contrib import admin
from django.contrib.admin import ModelAdmin

from shop.models import Product


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    pass

