from django.template import Library
from catalog.models import Product, Category
from django.conf import settings

register = Library()

@register.simple_tag
def company(option):
    if option == 'name':
        return settings.COMPANY_NAME
    if option == 'slogan':
        return settings.SLOGAN