from django.shortcuts import render
from django.views import View
from products.mixins import CartMixin

class IndexView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, "mainapp/index.html", {})
