# coding=utf-8

from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView, TemplateView
from django.forms import modelformset_factory
from django.contrib import messages
from django.urls import reverse
from time import sleep

from catalog.models import Product

from .models import CartItem


class CreateCartItemView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        if self.request.session.session_key is None:
            self.request.session.save()
        cart_item, created = CartItem.objects.add_item(self.request.session.session_key, product)
        if created:
            messages.success(self.request, 'Produto adicionado ao carrinho de compras!')
        else:
            messages.success(self.request, 'Produto atualizado no carrinho de compras!')
        sleep(0.5)        
        return product.get_absolute_url()

create_cart_item = CreateCartItemView.as_view()

class CartItemView(TemplateView):

    template_name = 'checkout/cart.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CartItemView, self).get_context_data(**kwargs)
        CartItemFormSet = modelformset_factory(CartItem, fields=('quantity',), can_delete=True, extra=0)
        session_key = self.request.session.session_key
        if session_key:
            context['formset'] = CartItemFormSet(queryset=CartItem.objects.filter(cart_key=session_key))
        else:
            context['formset'] = CartItemFormSet(queryset=CartItem.objects.filter(cart_key=CartItem.objects.none()))
        return context

cart_item = CartItemView.as_view()