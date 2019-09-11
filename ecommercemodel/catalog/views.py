# coding=utf-8

from django.shortcuts import render

from .models import Product, Category


def product_list(request, template_name = "catalog/product_list.html"):
    context = {
        "product_list" : Product.objects.all()
    }
    return render(request, template_name, context)

def category(request, slug, template_name = "catalog/category.html"):
    category = Category.objects.get(slug=slug)
    context = {
        "current_category" : category,
        "product_list" : Product.objects.filter(category=category)
    }
    return render(request, template_name, context)

def product(request, slug, template_name = "catalog/product.html"):
    product = Product.objects.get(slug=slug)
    context = {
        "product" : product,
    }
    return render(request, template_name, context)    