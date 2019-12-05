from django.shortcuts import render, get_object_or_404
from django.views.generic import RedirectView
from django.contrib import messages

from .models import CartItem
from catalog.models import Product

class CreateCartItemView(RedirectView):

    def det_redirect_url(self, *args, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        cart_item = CartItem.objects.add_item(self.request.session.session_key, product)
        messages.success(self.request, 'Produto adicionado ao carrinho de compras!')
        return product.get_absolute_url()

create_cart_item = CreateCartItemView.as_view()