# coding=utf-8

from django.db import models
from django.conf import settings


class CartItemManager(models.Manager):

    def add_item(self, cart_key, product):
        if self.filter(cart_key=cart_key, product=product).exists():
            created = False
            cart_item = self.get(cart_key=cart_key, product=product)
            cart_item.quantity = cart_item.quantity + 1
            cart_item.save()
        else:
            created = True
            cart_item = CartItem.objects.create(
                cart_key=cart_key, product=product, price=product.price)
        return cart_item, created


class CartItem(models.Model):

    cart_key = models.CharField('Chave do Carrinho', max_length=40, db_index=True)
    product = models.ForeignKey('catalog.Product', verbose_name='Produto', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=8)

    objects = CartItemManager()

    class Meta:
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens dos Carrinhos'
        unique_together = (('cart_key', 'product'),)

    def __str__(self):
        return f'{self.product} [{self.quantity}]'

class OrderManager(models.Manager):

    def create_order(self, user, cart_items):
        order = self.create(user=user)
        for cart_item in cart_items:
            order_item = OrderItem.objects.create(order=order, quantity=cart_item.quantity, 
            product=cart_item.product, price=cart_item.price)
        
        return order

class Order(models.Model):
    
    STATUS_CHOICES = (
        (0, 'Aguardando Pagamento'),
        (1, 'Pagamento Autorizado'),
        (2, 'Cuncluído'),
        (3, 'Cancelado'),
    )

    PAYMENT_OPTION_CHOICES = (
        ("deposito", 'Depósito em Conta'),
        ("boletobancario", 'Boleto Bancário'),
        ("pagseguro", 'PagSeguro'),
        ("paypal", 'PayPal'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete=models.CASCADE,)
    status = models.IntegerField('Situação', choices=STATUS_CHOICES, default=0, blank=True)
    payment_option = models.CharField('Modo de Pagamento', choices=PAYMENT_OPTION_CHOICES, max_length=30, default='deposito')
    created = models.DateTimeField('Data de Criação', auto_now_add=True)
    modified = models.DateTimeField('Data de Modificação', auto_now=True)
    
    objects = OrderManager()

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return f'Pedido #{self.pk:0>6}'

class OrderItem(models.Model):

    order = models.ForeignKey(Order, verbose_name="Pedido", related_name='Items', on_delete=models.CASCADE)
    product = models.ForeignKey('catalog.Product', verbose_name='Produto', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=8)

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens dos Pedidos'

    def __str__(self):
        return f'Pedido #{self.pk:0>6} - Produto {self.product}'


def post_save_cart_item(instance, **kwargs):
    if instance.quantity < 1:
        instance.delete()

models.signals.post_save.connect(post_save_cart_item, sender=CartItem, dispatch_uid='post_save_cart_item')