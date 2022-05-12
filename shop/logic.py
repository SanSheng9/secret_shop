
from django.db.models import Avg

from shop.models import UserProductRelation


def set_rating(product):
    rating = UserProductRelation.objects.filter(product=product).aggregate(rating=Avg('rate')).get('rating')
    product.rating = rating
    product.save()