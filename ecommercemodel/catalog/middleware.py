from .models import Product, ProductImages
from django.utils.timezone import now


def expirer_product_middleware(get_response):

    def middleware(request):
        # Before Middleware

        active_products = Product.objects.filter(is_active=True).filter(start_date__isnull=False).filter(end_date__isnull=False)
        inactive_products = Product.objects.filter(is_active=False).filter(start_date__isnull=False).filter(end_date__isnull=False)
        for product in inactive_products:
            if product.start_date <= now() and product.end_date > now():
                product.is_active = True
                product.save()
        for product in active_products:
            if product.start_date < now() and product.end_date < now():
                product.is_active = False
                product.save()

        response = get_response(request) # Middleware
        # After Middleware

            
        return response
    return middleware