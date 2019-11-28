# coding=utf-8

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView

from .forms import ContactForm


class IndexView(TemplateView): 

    template_name = "index.html"

index = IndexView.as_view()

def contact(request, template_name = "contact.html"):
    success = False
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.send_mail()
        success = True
        form = ContactForm()
    context = {
        'form': form,
        'sucesso' : success,
    }
    return render(request, template_name, context)