from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.timezone import now
from django.core.signals import request_started


class Category(models.Model):

    name = models.CharField("Nome", max_length=100)
    slug = models.SlugField('Identificador', max_length=100)

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta: 
        verbose_name = 'Categoria'
        verbose_name_plural = "Categorias"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:category', kwargs={'slug': self.slug})


class Product(models.Model):
    
    id = models.AutoField('Código', primary_key=True)
    name = models.CharField("Nome", max_length=100, blank=False, null=False, help_text="Obrigatório. Nome do Produto, de maior destaque na página.")
    slug = models.SlugField('Identificador', max_length=100, help_text="Não alterar esse campo.")
    category = models.ForeignKey('catalog.Category', related_name='Categoria', verbose_name="Categoria", on_delete=models.CASCADE, null=True, blank=False, help_text="Determine a categoria do produto.")
    description = models.TextField('Descrição', blank=False, null=False, max_length=85, help_text="Obrigatório. Uma descrição breve do Produto. Max. 85 caracteres.")
    description_big = models.TextField('Descrição Detalhada', blank=True, null=True, max_length=800, help_text="Opcional. Uma descrição longa do Produto. Max. 800 caracteres.")
    price = models.DecimalField("Preço", decimal_places=2, max_digits=8, help_text="Obrigatório. Determine um preço para o Produto.")
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)
    thumbnail = models.ImageField('Thumbnail do Produto', upload_to='products', blank=False, null=False, help_text="Obrigatório. Envie uma imagem para ser Thumbnail no produto. Thumbnails aparecem primeiro.")
    image2 = models.ImageField('Imagem 2', upload_to='products', blank=True, null=True, help_text="Opcional. Envie aqui fotos adicionais do produto.")
    image3 = models.ImageField('Imagem 3', upload_to='products', blank=True, null=True, help_text="Opcional. Envie aqui fotos do produto.")
    image4 = models.ImageField('Imagem 4', upload_to='products', blank=True, null=True, help_text="Opcional. Envie aqui fotos do produto.")
    # image = models.ForeignKey(ProductImages, verbose_name="Imagens",related_name="imagens", on_delete=models.CASCADE, null=True)
    start_date = models.DateTimeField('Data de Exibição', null=True, blank=True, help_text="Opcional, defina uma data futura, para que o Produto seja exibido somente a partir dela.", default=now)
    end_date = models.DateTimeField('Data de Expiração', null=True, blank=True, help_text="Opcional, defina uma data futura, para que o Produto deixe de ser exibido a partir dela.")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Criado por",related_name="criado_por", on_delete=models.CASCADE,)
    is_active = models.BooleanField("Ativo", default=True, help_text="Determina se esse Produto deve ser tratado como ativo. Desmarque isso em vez de excluir produtos.")
    spotlight = models.BooleanField("Destaque", default=False, help_text="Determina se esse Produto deve ser tratado como Destaque. Geralmente produtos em destaque possuem promoções.")


    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = "Produtos"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:product', kwargs={'slug': self.slug})

# class ProductImages(models.Model):

#     product = models.ForeignKey(Product, verbose_name="Produto",related_name="product", on_delete=models.CASCADE)
#     image = models.ImageField('Imagem', upload_to='products', blank=False, null=False, help_text="Obrigatório. Envie aqui uma foto do produto.")
#     spotlight_image = models.BooleanField("Destaque", default=False, help_text="Determina se essa imagem deve ser tratada como imagem de destaque no produto. Imagens de destaque aparecem primeiro.")
#     created = models.DateTimeField('Criado em', auto_now_add=True)
#     modified = models.DateTimeField('Modificado em', auto_now=True)

#     class Meta:
#         verbose_name = 'Imagem do produto'
#         verbose_name_plural = 'Imagens dos produtos'
#         ordering = ['product']

#     def __str__(self):
#         return f'Imagem de "{self.product}"'



# def request_started_product(instance, **kwargs):
#     if instance.end_date and instance.start_date:
#         if instance.start_date < now and instance.end_date > now:
#             instance.is_active = True
#             instance.save()
#             print("Ativando")
#         if instance.start_date < now and instance.end_date < now:
#             instance.is_active = False
#             print("Desativando")


# request_started.connect(request_started_product, sender=Product, dispatch_uid='request_started_product')
 