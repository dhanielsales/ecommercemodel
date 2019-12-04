# coding=utf-8

from django.urls import path

from accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path('', account, name="index"),
    path('registro/', register, name="register"),
    path('alterar-dados/', update_user, name="update_user"),

]
