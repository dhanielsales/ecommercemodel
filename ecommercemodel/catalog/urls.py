# coding=utf-8

from django.urls import path

from catalog.views import *

app_name = 'catalog'

urlpatterns = [
    path('', product_list, name="product_list"),
    path('<str:slug>', category, name="category"),
    path('<str:category_father>/<str:slug>', subcategory, name="subcategory"),
    path('produto/<str:slug>', product, name="product"),
]
