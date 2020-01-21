from django.contrib import admin


from .models import Product, Category, ProductImages, Subcategory

class CategoryAdmin(admin.ModelAdmin):

    list_display = ['name', 'slug', 'home_spotlight' ,'in_navbar', 'created', 'modified']
    search_fields = ['name', 'slug',]
    list_filter = ['created', 'modified']
    prepopulated_fields = {'slug': ('name',) }

class SubcategoryAdmin(admin.ModelAdmin):

    list_display = ['name', 'slug','category_father', 'created', 'modified']
    search_fields = ['name', 'slug', 'category_father__name']
    autocomplete_fields = ['category_father']
    list_filter = ['created', 'modified']
    prepopulated_fields = {'slug': ('name',)}

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
    extra = 1

class ProductAdmin(admin.ModelAdmin):

    def created_format(self, obj):
        return obj.created.strftime("%d/%m/%Y às %H:%M:%S")
    created_format.admin_order_field = 'created'

    def modified_format(self, obj):
        return obj.created.strftime("%d/%m/%Y às %H:%M:%S")
    modified_format.admin_order_field = 'modified'

    list_display = ['id', '__str__', 'price', 'category', 'subcategory', 'is_active', 'spotlight', 'created_format', 'modified_format', 'author']
    list_display_links = ('id', '__str__')
    search_fields = ['id', 'name', 'slug', 'category__name', 'subcategory__name']
    autocomplete_fields = ['category', 'subcategory']
    list_filter = ['created', 'modified',]
    inlines = [ProductImagesAdmin,] 
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ("Informações Básicas", {
            'fields': ('name', 'slug')
        }),
        ('Sobre o Produto', {
            'fields': (('category', 'subcategory'), 'price','description', 'description_big')
        }),
        ('Configurações do Produto', {
            'fields': (('start_date', 'end_date'), 'spotlight', 'is_active')
        }),
    )
    def category_autocomplete_fields(self, obj):
        return self.category.name

    def subcategory_autocomplete_fields(self, obj):
        return self.subcategory.name
        
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()
    # actions = []

admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Product, ProductAdmin)
