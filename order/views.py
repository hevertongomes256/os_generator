from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import render, redirect
from .models import Order, Checklist
from .forms import OrderForm, ChecklistItemFormSet
from .tools import initial_data_checklist


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'

    def get_queryset(self):
        # Para exibir apenas as orders do logista logado
        return Order.objects.all()


def order_create(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save()
            checklist = Checklist.objects.create(order=order)
            formset = ChecklistItemFormSet(request.POST, instance=checklist)
            if formset.is_valid():
                formset.save()
                return redirect('orders-list')
        else:
            formset = ChecklistItemFormSet(request.POST)
    else:
        order_form = OrderForm()
        checklist = Checklist()
        formset = ChecklistItemFormSet(instance=checklist, initial=initial_data_checklist)
    return render(request, 'orders/order_form.html', {
        'order_form': order_form,
        'formset': formset,
    })
