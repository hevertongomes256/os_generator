from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Order


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'

    def get_queryset(self):
        # Para exibir apenas as orders do logista logado
        return Order.objects.all()
