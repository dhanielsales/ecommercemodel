# coding=utf-8

from django.shortcuts import render, get_object_or_404
from django.views import generic 
from django.db import models
from watson import search as watson
from django.db.models import signals
# from django.views.decorators.cache import cache_page


from .models import Product, Category

class ProductListView(generic.ListView):

    template_name = "catalog/product_list.html"
    context_object_name = 'product_list'
    paginate_by = 3

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        q = self.request.GET.get('q', '')
        if q:
            if queryset.filter(models.Q(pk__iexact=q)):
                return queryset.filter(models.Q(pk__iexact=q))
            else:
                return watson.filter(queryset, q)
        return queryset


product_list = ProductListView.as_view()

class CategoryListView(generic.ListView):
    
    context_object_name = 'product_list'
    template_name = "catalog/category.html"
    paginate_by = 3

    def get_queryset(self):
        return Product.objects.filter(is_active=True, category__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['current_category'] = get_object_or_404(Category, slug=self.kwargs['slug'])
        return context

category = CategoryListView.as_view()

# @cache_page(60 * 1)
def product(request, slug, template_name = "catalog/product.html"):
    product = Product.objects.filter(is_active=True).get(slug=slug)
    context = {
        "product" : product,
    }
    return render(request, template_name, context)
