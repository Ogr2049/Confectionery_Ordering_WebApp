from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("delivery/", views.PayDeliveryView.as_view(), name="delivery"),
    path("contacts/", views.ContactView.as_view(), name="contacts"),
    path("receipts/", views.ReceiptsView.as_view(), name="receipts"),
    path("receipts/<str:slug>/", views.ReceiptDetailView.as_view(), name="detail_receipt"),
    path("create-receipt/", views.CreateReceiptView.as_view(), name="create_receipt"),
    path("delete-receipt/<int:id>", views.DeleteReceiptView.as_view(), name="delete_receipt"),
    path("update_like/", views.update_like, name="update_like"),
    path("edit_receipt/<int:id>", views.EditReceiptView.as_view(), name="edit_receipt")
]