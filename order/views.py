from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Order, Checklist
from .forms import OrderForm, ChecklistItemFormSet, ChecklistItemFormSetEdit,  OrderEditForm
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


def order_edit(request, pk):

    try:
        order = get_object_or_404(Order, pk=pk)
        checklist, created = Checklist.objects.get_or_create(order=order)

        if request.method == 'POST':
            order_form = OrderEditForm(request.POST, instance=order)
            formset = ChecklistItemFormSetEdit(request.POST, instance=checklist)
            if order_form.is_valid() and formset.is_valid():
                order_form.save()
                formset.save()
                return redirect('orders-list')
        else:
            order_form = OrderEditForm(instance=order)
            formset = ChecklistItemFormSetEdit(instance=checklist)

        return render(request, 'orders/order_form.html', {
            'order_form': order_form,
            'formset': formset,
            'object': order,
        })
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'orders/order_confirm_delete.html'
    success_url = reverse_lazy('orders-list')
