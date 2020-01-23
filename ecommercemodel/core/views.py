# coding=utf-8

import datetime

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy 

from .forms import ContactForm
from catalog.models import Product, Category

User = get_user_model()

class MyAuthForm(AuthenticationForm):
    error_messages = {
        'invalid_login': gettext_lazy(
            "Por favor, entre com um E-mail e Senha corretos. Note que ambos "
            "os campos diferenciam maiúsculas e minúsculas."
        ),
        'inactive': gettext_lazy("Essa conta está inativa."),
    }

class IndexView(TemplateView, LoginView):  

    template_name = "core/index.html"
    model = Product
    authentication_form = MyAuthForm

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        home_spotlights = Category.objects.filter(home_spotlight=True)
        context['home_spotlight'] = home_spotlights
        return context

index = IndexView.as_view()

def contact(request, template_name = "core/contact.html"):
    success = False
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.send_mail()
        success = True
        form = ContactForm()
    elif request.method == 'POST':
        messages.error(request, 'Formulário inválido!')
    context = {
        'form': form,
        'sucesso' : success,
    }
    return render(request, template_name, context)

