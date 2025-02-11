from .models import Cart, CartItem
from .views import _cart_id


def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))  # Filter the cart
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user)  # For authenticated users
            else:
                cart_items = CartItem.objects.filter(cart=cart[:1])  # For non-authenticated users
            for cart_item in cart_items:
                cart_count += cart_item.quantity  # Add quantity to the cart count
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)
