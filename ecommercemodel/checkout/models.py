from django.db import models

class CartItemManager(models.Manager):

    def add_item(self, cart_key, product):
        cart_item, created = self.get_or_create(product=product, cart_key=cart_key)
        if not created:
            cart_item.quantity = cart_item.quantity + 1
            cart_item.save()
        return cart_item

class CartItem(models.Model):

    cart_key = models.CharField('Chave do carrinho', max_length=40, db_index=True)
    product = models.ForeignKey('catalog.Product', verbose_name='Produto', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    price = models.DecimalField("Preço", decimal_places=2, max_digits=8)

    class Meta:
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens dos Carrinhos'
        unique_together = (('cart_key', 'product'),)

    objects = CartItemManager()

    def __str__(self):
        return f'{self.product} [{self.quantity}]'

