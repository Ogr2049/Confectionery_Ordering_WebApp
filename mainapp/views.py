from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from products.mixins import CartMixin
from . import models
from utils.parse_excel import parse_products

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
        new_cake = models.Cake.objects.create(full_name=data.get("name"), email=data.get("email"), address=data.get("address"), phone=data.get("phone"),
                                              amount=89100, comment=data.get("comment"), date_delivery=data.get("date-delivery"),
                                              time_delivery=data.get("time-delivery"), type_cake=data.get("specie-type"), form=data.get("form"))
        for key, value in data.items():
            if key.split("-")[0] == "floor":
                if new_cake.floors.filter(floor=int(key.split("-")[-1])).exists():
                    continue

                new_floor = models.Floor.objects.create(floor=int(key.split("-")[-1]))
                ingredient_default = models.Ingredient.objects.get(id=int(data.get(key)))
                new_floor.ingredients.add(ingredient_default)
                new_cake.amount += ingredient_default.price
                for k,v in data.items():
                    if k.split("-")[0] == "floor" and int(k.split("-")[-1]) == new_floor.floor and v != value:
                        ing = models.Ingredient.objects.get(id=data.get(k))
                        new_floor.ingredients.add(ing)
                        new_cake.amount += ing.price
                new_floor.save()
                new_cake.floors.add(new_floor)

        new_cake.save()
        request.user.cakes.add(new_cake)
        request.user.save()
        request.session["new_cake"] = new_cake.id
        sostav = ""
        for floor in new_cake.floors.all():
            sostav += f"Ярус {floor.floor}<br>"
            for ing in floor.ingredients.all():
                sostav += f"{ing.title}. Стоимость: {ing.price} р.<br><br>"
        send_mail(
            f"Новый заказ на торт на сайте Cake&Pie!",
            "",
            'robot@cake-pie-store.ru',
            ["lautariano777@gmail.com", "o.grigoriev2@yandex.ru"],
            html_message=f'''
                                                <p><b>Новый заказ на торт №{new_cake.id}</b><br>
                                                    <br>
                                                    Данные клиента:<br>
                                                    Имя: {new_cake.full_name}<br>
                                                    Номер телефона: {new_cake.phone}<br>
                                                    Почта: {new_cake.email}<br><br>
                                                    <b>Информация о заказе:</b><br>
                                                    Стоимость: <b>{new_cake.amount} рублей</b><br>
                                                    {new_cake.address}. {new_cake.date_delivery}. Время: {new_cake.time_delivery}<br>
                                                    Комментарий: {new_cake.comment}<br>
                                                    Тип торта: {new_cake.get_type_cake_display()}<br>
                                                    Форма торта: {new_cake.get_form_display()}<br>
                                                    <br><br>
                                                    <b>Состав заказа:</b><br>
                                                    {sostav}
                                                </p>
                                              '''
        )
        return redirect("success_cake")


class SuccessConstructorView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        cake = models.Cake.objects.get(id=request.session.get("new_cake"))
        return render(request, "mainapp/success_cake.html", {"cake": cake})