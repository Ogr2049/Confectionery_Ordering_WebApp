from django.http import JsonResponse
from django.shortcuts import render
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

class CatalogView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        products = models.Product.objects.all()
        category = None
        if "category" in request.GET.keys():
            category = models.Category.objects.get(slug=request.GET.get("category"))
            products = products.filter(category=category)
        if "q" in request.GET.keys():
            products = products.filter(title=request.GET.get("q"))
        return render(request, "products/catalog.html", {"products": products, "category": category})

class ProductDetailView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product = models.Product.objects.get(slug=kwargs.get("slug"))
        return render(request, "products/detail_product.html", {"product": product})