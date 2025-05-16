from django.urls import path
from . import views

urlpatterns = [
    path("catalog/", views.CatalogView.as_view(), name="catalog"),
    path("catalog/<str:slug>/", views.ProductDetailView.as_view(), name="detail_product"),
    path("order-sort", views.order_catalog, name="order-sort")
]