from django.urls import path
from . import views

urlpatterns = [
    path("catalog/", views.CatalogView.as_view(), name="catalog"),
    path("catalog/<str:slug>/", views.ProductDetailView.as_view(), name="detail_product"),
    path("order-sort", views.order_catalog, name="order-sort"),
    path("clear_cart/", views.ClearCartView.as_view(), name="clear_cart"),
    path("add_cart/", views.add_cart, name="add_cart"),
    path("cart/", views.CartView.as_view(), name="cart"),
    path("plus_cart/", views.plus_cart, name="plus_cart"),
    path("delete_product/", views.delete_cart, name="delete_product"),
    path("minus_cart/", views.minus_product_cart, name="minus_cart"),
]