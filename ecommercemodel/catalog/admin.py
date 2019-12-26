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

    fields = ('name', 'slug','category','description', 'description_big', 'price', 'image' , 'start_date', 'end_date', 'is_active')
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()
    # actions = []

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
