# coding=utf-8

from .models import Category

def categories(request):
    return {
        'categories': Category.objects.all(),
        'navcategories': Category.objects.filter(in_navbar=True),
    }

