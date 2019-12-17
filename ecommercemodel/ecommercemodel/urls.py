"""ecommercemodel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from core.views import *
from catalog.views import *
from accounts.views import *
from checkout.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name="index"),
    path('entrar/', LoginView.as_view(template_name='login.html'), name="login"),
    path('sair/', LogoutView.as_view(next_page='index'), name="logout"),
    path('contato/', contact, name="contact"),
    path('produtos/', include('catalog.urls', namespace="catalog")),
    path('conta/', include('accounts.urls', namespace="accounts")),
    path('compras/', include('checkout.urls', namespace="checkout")),
    path('paypal/', include('paypal.standard.ipn.urls')),
]
 