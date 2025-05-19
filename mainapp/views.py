from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from products.mixins import CartMixin
from . import models

class IndexView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, "mainapp/index.html", {})

class ContactView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, "mainapp/contacts.html", {})

class PayDeliveryView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, "mainapp/pay_delivery.html", {})

class ReceiptsView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        receipts = models.Receipt.objects.all()
        return render(request, "mainapp/receipts.html", {"receipts": receipts})

class ReceiptDetailView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        receipt = models.Receipt.objects.get(slug=kwargs.get("slug"))
        return render(request, "mainapp/detail_receipt.html", {"receipt": receipt})

class CreateReceiptView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("index")
        return render(request, "mainapp/create_receipt.html", {})

    def post(self, request, *args, **kwargs):
        data = request.POST
        new_receipt = models.Receipt.objects.create(author=request.user, title=data.get("title"),
                                                    cover=request.FILES.get("cover"), description=data.get("description"))
        new_receipt.save()
        return redirect("receipts")

class DeleteReceiptView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        receipt = models.Receipt.objects.get(id=kwargs.get("id"))
        if receipt.author == request.user:
            receipt.delete()
        return redirect("receipts")

def update_like(request):
    receipt = models.Receipt.objects.get(id=request.POST.get("receipt_id"))
    for like in receipt.likes.all():
        if like.user == request.user:
            receipt.likes.remove(like)
            receipt.save()
            return JsonResponse({"likes_count": receipt.likes.count()})
    new_like = models.Like.objects.create(user=request.user)
    new_like.save()
    receipt.likes.add(new_like)
    receipt.save()
    print(new_like)
    return JsonResponse({"likes_count": receipt.likes.count()})