from django.contrib import admin

from .models import CartItem, Order, OrderItem

class CartItemAdmin(admin.ModelAdmin):

    list_display = ['product', 'quantity', 'owner', 'price']
    search_fields = ['product', 'owner']

class OrderAdmin(admin.ModelAdmin):

    list_display = ['__str__', 'user', 'status', 'payment_option', 'created', 'modified',]
    search_fields = ['user', 'user', 'payment_option']

class OrderItemAdmin(admin.ModelAdmin):

    list_display = ['order', 'product', 'quantity', 'price',]
    search_fields = ['order', 'product']


admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
