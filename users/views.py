from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationForm
from django.views import View
from products.models import Cart
from products.mixins import CartMixin
from products.models import Product
import datetime
from django.core.mail import send_mail
from django.http import JsonResponse
from . import models
import random
import string

class LoginView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        context = {"form": form}

        return render(request, "users/login.html", context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect("profile")

        return render(request, "users/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('login')

class RegistrationView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {"form": form}

        return render(request, "users/signup.html", context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.email = form.cleaned_data["email"]
            new_user.phone = form.cleaned_data["phone"]
            new_user.full_name = form.cleaned_data["full_name"]
            new_user.save()
            new_cart = Cart.objects.create()
            new_cart.save()
            new_user.cart = new_cart
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()
            user = authenticate(email=new_user.email, password=form.cleaned_data["password"])
            login(request, user)
            return redirect("profile")
        return render(request, "users/signup.html", {"form": form})

class ProfileView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        return render(request, "users/cabinet.html", {})

    def post(self, request, *args, **kwargs):
        data = request.POST
        request.user.full_name = data["full_name"]
        request.user.phone = data.get("phone")
        request.user.email = data.get("email")
        request.user.save()
        return redirect("profile")

class MyOrdersView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        return render(request, "users/orders.html", {})
