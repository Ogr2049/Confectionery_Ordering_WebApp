from .models import Cart
from django.views import View

class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if not Cart.objects.filter(id=request.session.get("cart")).exists() and not request.user.is_authenticated:
            new_cart = Cart.objects.create()
            new_cart.save()
            request.session["cart"] = new_cart.id
        return super().dispatch(request, *args, **kwargs)
