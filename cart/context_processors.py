from .models import Cart

def cart_processor(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return {
            'cart_items_count': cart.items_count,
            'global_cart': cart
        }
    return {
        'cart_items_count': 0,
        'global_cart': None
    }
