# coding=utf-8

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect


from .forms import ContactForm

def index(request, template_name = "index.html"):
    return render(request, template_name)

def contact(request, template_name = "contact.html"):
    success = False
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.send_mail()
        success = True
        form = ContactForm()
    context = {
        'form': form,
        'success' : success,
    }
    return render(request, template_name, context)
 