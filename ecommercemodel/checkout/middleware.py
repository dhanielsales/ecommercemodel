from .models import CartItem

def cart_item_middleware(get_response):

    def middleware(request):
        # Before Middleware
        session_key = request.session.session_key

        if request.user.is_authenticated:
                session_user = request.user
                if CartItem.objects.filter(owner=session_user).exists():
                    if CartItem.objects.filter(owner=None ,cart_key=request.session.session_key):
                        for cart_item_authenticated in CartItem.objects.filter(owner=session_user):
                            for cart_item_anonymous in CartItem.objects.filter(owner=None ,cart_key=request.session.session_key):
                                if cart_item_authenticated.product == cart_item_anonymous.product:
                                    cart_item_authenticated.quantity += cart_item_anonymous.quantity
                                    cart_item_authenticated.save()
                                    cart_item_anonymous.delete()
                                else:
                                    cart_item_authenticated.cart_key = cart_item_anonymous.cart_key
                                    cart_item_authenticated.save()
                    else:
                        CartItem.objects.filter(owner=session_user).update(cart_key=request.session.session_key)

                CartItem.objects.filter(cart_key=request.session.session_key).update(owner=request.user)

        response = get_response(request) # Middleware
        # After Middleware

        if session_key != request.session.session_key and request.session.session_key:
            CartItem.objects.filter(cart_key=session_key).update(cart_key=request.session.session_key)
            
        return response
    return middleware