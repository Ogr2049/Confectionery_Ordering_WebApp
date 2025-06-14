from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from . import models
from .mixins import CartMixin

def order_catalog(request):
    products = models.Product.objects.all()
    if request.GET.get("category_slug") != "none":
        products = products.filter(category__slug=request.GET.get("category_slug"))
    products = products.order_by(request.GET.get("sort"))
    return JsonResponse({"products": [{"slug": product.slug, "image": product.image.url, "title": product.title, "id": product.id,
                                       "price": product.price, 'weight': product.weight} for product in products]})

class CatalogView(View):

    def get(self, request, *args, **kwargs):
        products = models.Product.objects.all()
        category = None
        if "category" in request.GET.keys():
            category = models.Category.objects.get(slug=request.GET.get("category"))
            products = products.filter(category=category)
        if "q" in request.GET.keys():
            products = products.filter(title__icontains=request.GET.get("q"))
        return render(request, "products/catalog.html", {"products": products, "category": category})

class ProductDetailView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product = models.Product.objects.get(slug=kwargs.get("slug"))
        return render(request, "products/detail_product.html", {"product": product})

class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            cart = request.user.cart
        else:
            cart = models.Cart.objects.get(id=request.session.get('cart'))
        return render(request, "products/cart.html", {"cart": cart})

class ClearCartView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            cart = request.user.cart
        else:
            cart = models.Cart.objects.get(id=request.session.get("cart"))
        cart.cart_products.clear()
        cart.total_price = 0
        cart.quantity_all = 0
        cart.save()
        return redirect("cart")


def add_cart(request):
    product_id = request.GET.get("product_id")
    product = models.Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart = request.user.cart
    else:
        cart = models.Cart.objects.get(id=request.session.get('cart'))

    for cart_product in cart.cart_products.all():
        if cart_product.product == product:
            cart_product.total_price += product.price
            cart_product.quantity += 1
            cart.quantity_all += 1
            cart.total_price += product.price
            cart.total_price = round(cart.total_price, 2)
            cart.save()
            cart_product.save()
            return JsonResponse({'count': cart.quantity_all})

    new_cartproduct = models.CartProduct.objects.create(product=product, quantity=1,
                                                        total_price=product.price)
    new_cartproduct.save()
    cart.cart_products.add(new_cartproduct)
    cart.quantity_all += 1
    cart.total_price += new_cartproduct.total_price
    cart.total_price = round(cart.total_price, 2)
    cart.save()

    return JsonResponse({'count': cart.quantity_all})


def delete_cart(request):
    cart_product = models.CartProduct.objects.get(id=request.GET.get("cart_product_id"))

    if request.user.is_authenticated:
        cart = request.user.cart
    else:
        cart = models.Cart.objects.get(id=request.session.get('cart'))

    cart.quantity_all -= cart_product.quantity
    cart.total_price -= cart_product.total_price
    cart_product.delete()
    cart.total_price = round(cart.total_price, 2)
    cart.save()
    return JsonResponse({'quantity_all': cart.quantity_all, "total_price": cart.total_price, "cart_products": [
        {"id": cart_product.id, "product_id": cart_product.product.id, "slug": cart_product.product.slug,
         "price": cart_product.product.price,"image": cart_product.product.image.url,
         "quantity": cart_product.quantity, "total_price": cart_product.total_price,
         "title": cart_product.product.title}
        for cart_product in cart.cart_products.all()]})


def plus_cart(request):
    cart_product = models.CartProduct.objects.get(id=request.GET.get("cart_product_id"))

    if request.user.is_authenticated:
        cart = request.user.cart
    else:
        cart = models.Cart.objects.get(id=request.session.get('cart'))

    if request.GET.get("quantity") == "false":
        cart_product.total_price += cart_product.product.price
        cart_product.quantity += 1
        cart.quantity_all += 1
        cart.total_price += cart_product.product.price
    else:
        cart.total_price -= cart_product.total_price
        cart_product.total_price = cart_product.product.price * int(request.GET.get("quantity"))
        cart.quantity_all -= cart_product.quantity
        cart_product.quantity = int(request.GET.get("quantity"))
        cart.total_price += cart_product.total_price
        cart.quantity_all += cart_product.quantity
    cart.total_price = round(cart.total_price, 2)
    cart_product.total_price = round(cart_product.total_price, 2)
    cart.save()
    cart_product.save()
    return JsonResponse({'quantity_all': cart.quantity_all, "total_price": cart.total_price, "cart_products": [
        {"id": cart_product.id,
         "product_id": cart_product.product.id, "slug": cart_product.product.slug,
         "price": cart_product.product.price, "image": cart_product.product.image.url,
         "quantity": cart_product.quantity, "total_price": cart_product.total_price,
         "title": cart_product.product.title}
        for cart_product in cart.cart_products.all()]})


def minus_product_cart(request):
    cart_product = models.CartProduct.objects.get(id=request.GET.get("cart_product_id"))
    if request.user.is_authenticated:
        cart = request.user.cart
    else:
        cart = models.Cart.objects.get(id=request.session.get('cart'))
    if cart_product.quantity == 1:
        cart.cart_products.remove(cart_product)
        cart.quantity_all -= cart_product.quantity
        cart.total_price -= cart_product.total_price
        cart_product.delete()
    else:
        cart_product.quantity -= 1
        cart_product.total_price -= cart_product.product.price
        cart.quantity_all -= 1
        cart.total_price -= cart_product.product.price
        cart_product.total_price = round(cart_product.total_price, 2)
        cart_product.save()
    cart.total_price = round(cart.total_price, 2)
    cart.save()
    return JsonResponse({'quantity_all': cart.quantity_all, "total_price": cart.total_price, "cart_products": [
        {"id": cart_product.id, "product_id": cart_product.product.id, "slug": cart_product.product.slug,
         "image": cart_product.product.image.url,
         "quantity": cart_product.quantity,
         "price": cart_product.product.price,
         "total_price": cart_product.total_price, "title": cart_product.product.title}
        for cart_product in cart.cart_products.all()]})

class OrderView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            cart = request.user.cart
        else:
            return redirect("login")
        return render(request, "products/order.html", {"cart": cart})

    def post(self, request, *args, **kwargs):
        data = request.POST
        cart = request.user.cart
        new_order = models.Order.objects.create(full_name=data.get("name"), phone=data.get("phone"),
                                                email=data.get("email"), type_pay=data.get("buy"),
                                                comment=data.get("comment"), quantity_all=cart.quantity_all)
        new_delivery = models.Delivery.objects.create(date_delivery=data.get("date-delivery"))
        if data.get("delivery-type") == "courier":
            new_delivery.address = data.get("address")
            new_order.amount = cart.total_price + 300
        else:
            new_delivery.pvz = data.get("pvz")
            new_order.amount = cart.total_price
        new_delivery.save()
        new_order.delivery = new_delivery

        for cart_product in cart.cart_products.all():
            new_order.products.add(cart_product)
        new_order.save()
        request.user.orders.add(new_order)
        request.user.save()
        request.session["new_order"] = new_order.id
        sostav = ""
        for cart_product in new_order.products.all():
            sostav += f"{cart_product.product.title} {cart_product.quantity} шт. Стоимость: {cart_product.total_price} р.<br>"
        send_mail(
            f"Новый заказ на сайте Cake&Pie!",
            "",
            'robot@cake-pie-store.ru',
            ["lautariano777@gmail.com", "o.grigoriev2@yandex.ru"],
            html_message=f'''
                                        <p><b>Новый заказ №{new_order.id}</b><br>
                                            <br>
                                            Данные клиента:<br>
                                            Имя: {new_order.full_name}<br>
                                            Номер телефона: {new_order.phone}<br>
                                            Почта: {new_order.email}<br><br>
                                            <b>Информация о заказе:</b><br>
                                            Стоимость: <b>{new_order.amount} рублей</b><br>
                                            {new_order.delivery}<br>
                                            Способ оплаты: {new_order.get_type_pay_display()}<br>
                                            Комментарий: {new_order.comment}<br>
                                            <br><br>
                                            <b>Состав заказа:</b><br>
                                            {sostav}
                                        </p>
                                      '''
        )
        return redirect("success")

class SuccessView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        order = models.Order.objects.get(id=request.session.get("new_order"))
        return render(request, "products/success.html", {"order": order})