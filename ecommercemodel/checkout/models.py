# coding=utf-8
from django.db import models
from django.conf import settings

from pagseguro.api import PagSeguroItem, PagSeguroApi
from pagseguro.signals import notificacao_recebida

from catalog.models import Product


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
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete=models.CASCADE, null=True)

    objects = CartItemManager()

    class Meta:
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens dos Carrinhos'
        unique_together = (('cart_key', 'product'),)

    def __str__(self):
        return f'{self.product}'

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
        (2, 'Concluído'),
        (3, 'Cancelado'),
    )

    PAYMENT_OPTION_CHOICES = (
        ("boletobancario", 'Boleto Bancário'),
        ("pagseguro", 'PagSeguro'),
        ("paypal", 'PayPal'),
    )

    id = models.AutoField('ID do Pedido', primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete=models.CASCADE,)
    status = models.IntegerField('Situação', choices=STATUS_CHOICES, default=0, blank=True)
    payment_option = models.CharField('Modo de Pagamento', choices=PAYMENT_OPTION_CHOICES, max_length=30, default=None, blank=True, null=True)
    created = models.DateTimeField('Data de Criação', auto_now_add=True)
    modified = models.DateTimeField('Data de Modificação', auto_now=True)
    
    objects = OrderManager()

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def products(self):
        products_ids = self.items.values_list('product')
        return Product.objects.filter(pk__in=products_ids)
    
    def total_price(self):
        aggregate_queryset = self.items.aggregate(total=models.Sum(models.F('price')
         * models.F('quantity'), output_field=models.DecimalField()))
        return aggregate_queryset['total']

    def pagseguro(self):
        self.payment_option = 'pagseguro'
        self.save()
        pg = PagSeguroApi(reference=self.id, 
                          token=settings.PAGSEGURO_TOKEN, 
                          email=settings.PAGSEGURO_EMAIL,
                          senderEmail=self.user.email, 
                          senderName=self.user.name)
        for item in self.items.all():
            pagseg_item = PagSeguroItem(id=item.product.pk, 
                                        description=item.product.name,
                                        amount=f'{item.price:.2f}',
                                        quantity=item.quantity,
                                        shipping_cost=None, 
                                        weight=None)
            pg.add_item(pagseg_item)
        return pg

    def __str__(self):
        return f'#{self.id:0>6}'

class OrderItem(models.Model):

    order = models.ForeignKey(Order, verbose_name="Pedido", related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('catalog.Product', verbose_name='Produto', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=8)

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens dos Pedidos'

    def __str__(self):
        return f'Pedido #{self.pk:0>6} - Produto {self.product}'

#### Signals

## Excluir item ao zerar
def post_save_cart_item(instance, **kwargs):
    if instance.quantity < 1:
        instance.delete()

models.signals.post_save.connect(post_save_cart_item, sender=CartItem, dispatch_uid='post_save_cart_item')

## PagSeguro

def load_signal(sender, data, **kwargs):
    print(data['success'])

checkout_realizado.connect(load_signal, sender=Order)

def load_signal(sender, data, **kwargs):
    print(data['success'])

checkout_realizado.connect(load_signal, sender=Order)