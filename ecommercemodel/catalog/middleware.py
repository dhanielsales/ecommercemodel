from .models import Product

def expirer_product_middleware(get_response):

    def middleware(request):
        # Before Middleware
        
        # active_queryset = Product.objects.filter(is_active=True)
        # inactive_queryset = Product.objects.filter(is_active=False)



        # if instance.end_date and instance.start_date:
        #     if instance.start_date < now and instance.end_date > now:
        #         instance.is_active = True
        #         instance.save()
        #         print("Ativando")
        #     if instance.start_date < now and instance.end_date < now:
        #         instance.is_active = False
        #         print("Desativando")

        response = get_response(request) # Middleware
        # After Middleware

            
        return response
    return middleware