# coding=utf-8

from django.urls import path

from checkout.views import *

app_name = 'checkout'

urlpatterns = [
    path('carrinho/adicionar/<str:slug>', create_cart_item, name="create_cart_item"),
    path('carrinho/', cart_item, name="cart_item"),
    path('finalizando/', checkout_order, name="checkout_order"),
    path('finalizando/pagseguro/<slug:pk>', pagseguro_view, name="pagseguro_view"),
]
