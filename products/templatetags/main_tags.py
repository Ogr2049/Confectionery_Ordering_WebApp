from django import template
from products import models

register = template.Library()

@register.simple_tag()
def get_cart_count(request):
    if request.user.is_authenticated:
        cart = request.user.cart
    else:
        cart = models.Cart.objects.get(id=request.session.get('cart'))
    return cart.cart_products.count()

@register.simple_tag()
def get_cart(request):
    if request.user.is_authenticated:
        cart = request.user.cart
    else:
        cart = models.Cart.objects.get(id=request.session.get('cart'))
    return cart

register = template.Library()

@register.simple_tag()
def get_categories():
    categories = models.Category.objects.all()
    return categories