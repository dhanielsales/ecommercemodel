from django.template import Library
from catalog.models import Category, Subcategory

register = Library()

@register.filter
def navbar_subcategories(category_father):
    return Subcategory.objects.filter(category_father=category_father)
