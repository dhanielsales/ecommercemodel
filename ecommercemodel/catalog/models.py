from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.timezone import now
from django.core.signals import request_started

class Category(models.Model):

    name = models.CharField("Nome", max_length=100, unique=True, help_text='Determine uma subcategoria para que possa ser associada ao produtos.')
    slug = models.SlugField('Identificador', max_length=100)
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)
    image = models.ImageField('Imagem', upload_to='categories', blank=True, null=True, help_text="Opcional. Envie uma foto para a categoria.")
    home_spotlight = models.BooleanField("Destaque na página inicial", default=False, help_text="Determina se essa Categoria deve ser inclusa nos Destaques da Página Inicial. Geralmente Categoria em destaque possuem promoções.")
    in_navbar = models.BooleanField("Incluir na Barra Superior?", default=False, help_text="Determina se essa Categoria deve ser inclusa na barra superior do site.")


    class Meta: 
        verbose_name = 'Categoria'
        verbose_name_plural = "Categorias"
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('catalog:category', kwargs={'slug': self.slug})

class Subcategory(models.Model):

    name = models.CharField("Nome", max_length=100)
    slug = models.SlugField('Identificador', max_length=100)
    category_father = models.ForeignKey('catalog.Category', verbose_name="Categoria", on_delete=models.CASCADE,null=False, blank=False, help_text="Determine a categoria o essa subcategoria será associada.")
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta: 
        verbose_name = 'Subcategoria'
        verbose_name_plural = "Subcategorias"
        unique_together = (('name', 'category_father'),)
        ordering = ['name']

    def __str__(self):
        return f'{self.category_father} - {self.name}'
        # return self.name

    def get_absolute_url(self):
        pass

class Product(models.Model):
    
    id = models.AutoField('Código', primary_key=True)
    name = models.CharField("Nome", max_length=100, blank=False, null=False, unique=True, help_text="Obrigatório. Nome do Produto, de maior destaque na página.")
    slug = models.SlugField('Identificador', max_length=100, help_text="Não alterar esse campo.")
    category = models.ForeignKey('catalog.Category', related_name='category', verbose_name="Categoria", on_delete=models.CASCADE, null=True, blank=False, help_text="Determine uma categoria para o produto.")
    subcategory = models.ForeignKey('catalog.Subcategory', verbose_name="Subcategoria", on_delete=models.CASCADE, null=True, blank=False, help_text="Determine uma subcategoria para o produto.")
    description = models.TextField('Descrição', blank=False, null=False, max_length=85, help_text="Obrigatório. Uma descrição breve do Produto. Max. 85 caracteres.")
    description_big = models.TextField('Descrição Detalhada', blank=True, null=True, max_length=800, help_text="Opcional. Uma descrição longa do Produto. Max. 800 caracteres.")
    price = models.DecimalField("Preço", decimal_places=2, max_digits=8, help_text="Obrigatório. Determine um preço para o Produto.")
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)
    start_date = models.DateTimeField('Data de Exibição', null=True, blank=True, help_text="Opcional, defina uma data futura, para que o Produto seja exibido somente a partir dela.")
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

class ProductImages(models.Model):

    product = models.ForeignKey(Product, verbose_name="Produto", related_name="images", on_delete=models.CASCADE)
    image = models.ImageField('Imagem', upload_to='products', blank=False, null=False, help_text="Obrigatório. Envie uma foto para o produto.")
    thumbnail = models.BooleanField("Thumbnail", default=False, help_text="Determina se essa imagem deve ser tratada como thumbnail do produto. Thumbnail aparecem primeiro.")
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Imagem'
        verbose_name_plural = 'Imagens'
        # unique_together = (('product', 'thumbnail'),)


    def __str__(self):
        return f'Imagem de "{self.product}"'

