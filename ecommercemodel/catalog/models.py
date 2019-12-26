from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.timezone import now


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
    description = models.TextField('Descrição', blank=True, max_length=85, help_text="Obrigatório. Uma descrição breve do Produto. Max. 85 caracteres.")
    description_big = models.TextField('Descrição detalhada', blank=True, null=True, max_length=800, help_text="Opcional. Uma descrição longa do Produto. Max. 800 caracteres.")
    price = models.DecimalField("Preço", decimal_places=2, max_digits=8, help_text="Obrigatório. Determine um preço para o Produto.")
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)
    image = models.ImageField('Imagem', upload_to='products', blank=True, null=True, help_text="Obrigatório. Envie aqui fotos do produto.")
    start_date = models.DateTimeField('Data de exibição', null=True, blank=True, help_text="Opcional, defina uma data futura, para que o Produto seja exibido somente a partir dela.", default=now)
    end_date = models.DateTimeField('Data de expiração', null=True, blank=True, help_text="Opcional, defina uma data futura, para que o Produto deixe de ser exibido a partir dela.")
    # author = models.CharField("Criado por", max_length=30, null=False, blank=False, default='', editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Criado por",related_name="criado_por", on_delete=models.CASCADE,)
    is_active = models.BooleanField("Ativo", default=True, help_text="Determina se esse Produto deve ser tratado como ativo. Desmarque isso em vez de excluir produtos.")

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = "Produtos"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:product', kwargs={'slug': self.slug})

# def request_started_product(instance, **kwargs):
#     if start_date < now:
#         instance.delete()

# models.signals.post_save.connect(request_started_product, sender=Product, dispatch_uid='request_started_product')
