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
        if "q" in request.GET.keys():
            receipts = receipts.filter(title__icontains=request.GET.get("q"))
        if "receipts" in request.GET.keys():
            receipts = receipts.filter(author=request.user)
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

class EditReceiptView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        receipt = models.Receipt.objects.get(id=kwargs.get("id"))
        if receipt.author != request.user:
            return redirect("receipts")
        return render(request, "mainapp/edit_receipt.html", {"receipt": receipt})

    def post(self, request, *args, **kwargs):
        receipt = models.Receipt.objects.get(id=kwargs.get("id"))
        data = request.POST
        receipt.title=data.get("title")
        if "cover" in request.FILES.keys():
            receipt.cover=request.FILES.get("cover")
        receipt.description=data.get("description")
        receipt.save()
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

class ConstructorView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ing_categories = models.CategoryIngredient.objects.all()
        return render(request, "mainapp/constructor.html", {"ing_categories": ing_categories})

    def post(self, request, *args, **kwargs):
        data = request.POST
        print(data)
        new_cake = models.Cake.objects.create(full_name=data.get("name"), email=data.get("email"), phone=data.get("phone"),
                                              amount=89100, comment=data.get("comment"), date_delivery=data.get("date-delivery"),
                                              time_delivery=data.get("time-delivery"), type_cake=data.get("specie-type"), form=data.get("form"))
        for key, value in data.items():
            if key.split("-")[0] == "floor":
                if new_cake.floors.filter(floor=int(key.split("-")[-1])).exists():
                    continue

                new_floor = models.Floor.objects.create(floor=int(key.split("-")[-1]))
                for ing_id in data.getlist(key):
                    ingredient_default = models.Ingredient.objects.get(id=int(ing_id))
                    new_floor.ingredients.add(ingredient_default)
                    new_cake.amount += ingredient_default.price
                for k,v in data.items():
                    if k.split("-")[0] == "floor" and int(k.split("-")[-1]) == new_floor.floor and v != value:
                        for ing_id in data.getlist(k):
                            ing = models.Ingredient.objects.get(id=int(ing_id))
                            new_floor.ingredients.add(ing)
                            new_cake.amount += ing.price
                new_floor.save()
                new_cake.floors.add(new_floor)

        new_cake.save()
        request.session["new_cake"] = new_cake.id
        return redirect("success_cake")


class SuccessConstructorView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        cake = models.Cake.objects.get(id=request.session.get("new_cake"))
        return render(request, "mainapp/success_cake.html", {"cake": cake})