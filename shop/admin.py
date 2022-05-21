from django.contrib import admin
from django.contrib.admin import ModelAdmin

from shop.models import Product, UserProductRelation, UserProfile


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    pass

@admin.register(UserProfile)
class UserProfileAdmin(ModelAdmin):
    pass

@admin.register(UserProductRelation)
class UserProductRelationAdmin(ModelAdmin):
    pass
