from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum, Count, Avg
from django.views.generic import ListView
from django.views.generic.edit import DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import datetime, timedelta
from django.urls import reverse_lazy
from .models import Order, Checklist
from .forms import OrderForm, ChecklistItemFormSet, ChecklistItemFormSetEdit,  OrderEditForm
from .tools import initial_data_checklist
from .pdfreport import generate_pdf_entry, generate_pdf_exit
from .forms import OrderFilterForm
import json


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 15

    def get_queryset(self):
        queryset = Order.objects.filter(
            created_by=self.request.user
        ).select_related('client').prefetch_related('checklist')

        # Aplicar filtros
        self.filter_form = OrderFilterForm(self.request.GET, user=self.request.user)

        if self.filter_form.is_valid():
            queryset = self.apply_filters(queryset, self.filter_form.cleaned_data)

        return queryset.order_by('-shipping_date')

    def apply_filters(self, queryset, cleaned_data):
        # Filtro de busca textual
        search = cleaned_data.get('search')
        if search:
            queryset = queryset.filter(
                Q(client__first_name__icontains=search) |
                Q(device__icontains=search) |
                Q(defect__icontains=search) |
                Q(id__icontains=search)
            )

        # Filtro por cliente
        client = cleaned_data.get('client')
        if client:
            queryset = queryset.filter(client=client)

        # Filtro por período
        period = cleaned_data.get('period')
        if period:
            now = timezone.now()
            if period == 'today':
                queryset = queryset.filter(shipping_date__date=now.date())
            elif period == 'week':
                start_week = now - timedelta(days=now.weekday())
                queryset = queryset.filter(shipping_date__gte=start_week)
            elif period == 'month':
                queryset = queryset.filter(
                    shipping_date__year=now.year,
                    shipping_date__month=now.month
                )
            elif period == 'quarter':
                quarter_start = datetime(now.year, ((now.month-1)//3)*3 + 1, 1)
                queryset = queryset.filter(shipping_date__gte=quarter_start)
            elif period == 'year':
                queryset = queryset.filter(shipping_date__year=now.year)

        # Filtro por status
        status = cleaned_data.get('status')
        if status:
            if status == 'pending':
                queryset = queryset.filter(
                    service_autorized=False, 
                    withdrawal_date__isnull=True
                )
            elif status == 'authorized':
                queryset = queryset.filter(
                    service_autorized=True, 
                    withdrawal_date__isnull=True
                )
            elif status == 'completed':
                queryset = queryset.filter(withdrawal_date__isnull=False)

        # Filtro por valor
        min_value = cleaned_data.get('min_value')
        max_value = cleaned_data.get('max_value')
        if min_value:
            queryset = queryset.filter(service_total__gte=min_value)
        if max_value:
            queryset = queryset.filter(service_total__lte=max_value)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_orders = Order.objects.filter(created_by=self.request.user)

        # Form de filtros
        context['filter_form'] = getattr(self, 'filter_form', OrderFilterForm(user=self.request.user))

        # Métricas financeiras
        context.update(self.calculate_financial_metrics(user_orders))

        # Dados para gráficos
        context['chart_data'] = self.get_chart_data(user_orders)

        return context

    def calculate_financial_metrics(self, orders):
        """Calcula métricas financeiras das ordens"""
        # Total ganho (ordens concluídas)
        total_earned = orders.filter(
            withdrawal_date__isnull=False
        ).aggregate(total=Sum('service_total'))['total'] or 0

        # Total a receber (ordens autorizadas mas não retiradas)
        total_pending = orders.filter(
            service_autorized=True,
            withdrawal_date__isnull=True
        ).aggregate(total=Sum('service_total'))['total'] or 0

        # Valor em andamento (não autorizadas)
        total_in_progress = orders.filter(
            service_autorized=False,
            withdrawal_date__isnull=True
        ).aggregate(total=Sum('service_total'))['total'] or 0

        # Valor médio por ordem
        avg_order_value = orders.aggregate(
            avg=Avg('service_total')
        )['avg'] or 0

        # Estatísticas de status
        total_orders = orders.count()
        completed_orders = orders.filter(withdrawal_date__isnull=False).count()
        pending_orders = orders.filter(
            service_autorized=False, 
            withdrawal_date__isnull=True
        ).count()
        authorized_orders = orders.filter(
            service_autorized=True, 
            withdrawal_date__isnull=True
        ).count()
        
        return {
            'total_earned': total_earned,
            'total_pending': total_pending,
            'total_in_progress': total_in_progress,
            'avg_order_value': avg_order_value,
            'total_orders': total_orders,
            'completed_orders': completed_orders,
            'pending_orders': pending_orders,
            'authorized_orders': authorized_orders,
        }

    def get_chart_data(self, orders):
        """Prepara dados para os gráficos"""
        # Dados dos últimos 12 meses
        twelve_months_ago = timezone.now() - timedelta(days=365)

        monthly_data = orders.filter(
            shipping_date__gte=twelve_months_ago
        ).annotate(
            month=TruncMonth('shipping_date')
        ).values('month').annotate(
            count=Count('id'),
            total_value=Sum('service_total'),
            completed_count=Count('id', filter=Q(withdrawal_date__isnull=False))
        ).order_by('month')
        
        # Formatar dados para Chart.js
        months = []
        order_counts = []
        order_values = []
        completed_counts = []
        
        for data in monthly_data:
            if data['month']:
                months.append(data['month'].strftime('%b/%Y'))
                order_counts.append(data['count'])
                order_values.append(float(data['total_value'] or 0))
                completed_counts.append(data['completed_count'])
 
        return {
            'months': json.dumps(months),
            'order_counts': json.dumps(order_counts),
            'order_values': json.dumps(order_values),
            'completed_counts': json.dumps(completed_counts),
        }


def order_create(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST, user=request.user)

        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.created_by = request.user
            order.save()
            checklist = Checklist.objects.create(order=order)
            formset = ChecklistItemFormSet(request.POST, instance=checklist)
            if formset.is_valid():
                formset.save()
                return redirect('orders-list')
        else:
            formset = ChecklistItemFormSet(request.POST)
    else:
        order_form = OrderForm(user=request.user)
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
            order_form = OrderEditForm(request.POST, instance=order, user=request.user)
            formset = ChecklistItemFormSetEdit(request.POST, instance=checklist)
            if order_form.is_valid() and formset.is_valid():
                order_form.save()
                formset.save()
                return redirect('orders-list')
        else:
            order_form = OrderEditForm(instance=order, user=request.user)
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


def generate_pdf_os(request, order_id):
    tipo = request.GET.get('type')
    order = get_object_or_404(Order, id=order_id)
    checklist = order.checklist

    if tipo == 'entrada':
        return generate_pdf_entry(order, checklist)
    elif tipo == 'saida':
        return generate_pdf_exit(order, checklist)
    else:
        return HttpResponseBadRequest("Tipo não informado ou inválido.")
