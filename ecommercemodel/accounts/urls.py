# coding=utf-8

from django.urls import path

from accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path('', account, name="account"),
    path('registro/', register, name="register"),
    path('alterar-dados/', update_user, name="update_user"),
    path('alterar-senha/', update_password, name="update_password"),

]
