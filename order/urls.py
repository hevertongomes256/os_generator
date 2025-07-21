# orders/urls.py
from django.urls import path
from .views import OrderListView, OrderDeleteView, order_edit, order_create

urlpatterns = [
    path('', OrderListView.as_view(), name='orders-list'),
    path('orders/new/', order_create, name='order-create'),
    path('orders/<int:pk>/edit/', order_edit, name='order-edit'),
    path('orders/<int:pk>/deletar/', OrderDeleteView.as_view(), name='order-delete'),
]
