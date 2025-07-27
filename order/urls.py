# orders/urls.py
from django.urls import path
from .views import OrderListView, OrderDeleteView, order_edit, order_create, generate_pdf_os

urlpatterns = [
    path('', OrderListView.as_view(), name='orders-list'),
    path('new/', order_create, name='order-create'),
    path('<int:pk>/edit/', order_edit, name='order-edit'),
    path('<int:pk>/deletar/', OrderDeleteView.as_view(), name='order-delete'),
    path('generate_pdf/<int:order_id>/', generate_pdf_os, name='generate_pdf_os'),
]
