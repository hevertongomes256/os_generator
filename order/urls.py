# orders/urls.py
from django.urls import path
from .views import OrderListView, order_edit, order_create

urlpatterns = [
    path('', OrderListView.as_view(), name='orders-list'),
    path('orders/new/', order_create, name='order-create'),
    path('orders/<int:pk>/edit/', order_edit, name='order-edit'),
]
