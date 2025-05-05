from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.RegistrationView.as_view(), name="register"),
    path("orders/", views.MyOrdersView.as_view(), name="orders"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("logout/", views.logout_view, name="logout")
]