# coding=utf-8

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

def index(request, template_name = "index.html"):
    return render(request, template_name)

def contact(request, template_name = "contact.html"):
    return render(request, template_name)
