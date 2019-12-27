from django.contrib import admin

from .models import Product, Category

class CategoryAdmin(admin.ModelAdmin):

    list_display = ['name', 'slug', 'created', 'modified']
    search_fields = ['name', 'slug']
    list_filter = ['created', 'modified']
    prepopulated_fields = {'slug': ('name',) }

class ProductAdmin(admin.ModelAdmin):

    list_display = ['id', '__str__', 'slug', 'price', 'category','is_active', 'created', 'modified', 'author']
    search_fields = ['id', 'name', 'slug', 'category__name']
    list_filter = ['created', 'modified',]
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ("Informações Básicas", {
            'fields': ('name', 'slug')
        }),
        ('Sobre o Produto', {
            'fields': ('category', 'price','description', 'description_big')
        }),
        ('Imagens do Produto', {
            'fields': ('thumbnail', 'image2', 'image3', 'image4')
        }),
        ('Configurações do Produto', {
            'fields': ('start_date', 'end_date', 'spotlight', 'is_active')
        }),
    )
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()
    # actions = []

# class ProductImagesAdmin(admin.ModelAdmin):
#     list_display = ['product', 'image', 'spotlight_image']
#     search_fields = ['product']
#     list_filter = ['created', 'modified',]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
# admin.site.register(ProductImages, ProductImagesAdmin)
