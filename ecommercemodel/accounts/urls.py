# coding=utf-8

from django.urls import path

from accounts.views import *
from checkout.views import order_list, order_detail


app_name = 'accounts'

urlpatterns = [
    path('', account, name="account"),
    path('registro/', register, name="register"),
    path('alterar-dados/', update_user, name="update_user"),
    path('alterar-senha/', update_password, name="update_password"),
    path('meus-pedidos/', order_list, name="order_list"),
    path('meus-pedidos/<slug:pk>', order_detail, name="order_detail"),


]
