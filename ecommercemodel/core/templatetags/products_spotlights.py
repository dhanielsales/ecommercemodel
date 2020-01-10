from django.template import Library
from catalog.models import Product, Category

register = Library()

@register.filter
def products_spotlights(category):
    return Product.objects.filter(is_active=True, spotlight=True, category=category)