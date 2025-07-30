from django import forms
from django.forms import inlineformset_factory
from person.models import Person
from .models import Order, Checklist, ChecklistItem
from .tools import initial_data_checklist


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'device', 'defect', 'additional_info', 'additional_description', 'service_total',
                  'service_initial', 'missing_payment', 'service_autorized']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['client'].queryset = Person.objects.filter(owner=user, person_type=2)


ChecklistItemFormSet = inlineformset_factory(
    Checklist,
    ChecklistItem,
    fields=['description', 'checked'],
    extra=len(initial_data_checklist),
    can_delete=False
)


class OrderEditForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'device', 'defect', 'additional_info', 'additional_description', 'service_total',
                  'service_initial', 'missing_payment', 'service_autorized', 'name_withdrawal', 'withdrawal_date']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['client'].queryset = Person.objects.filter(owner=user, person_type=2)


ChecklistItemFormSetEdit = inlineformset_factory(
    Checklist,
    ChecklistItem,
    fields=['description', 'checked'],
    extra=0,
    can_delete=False
)


class OrderFilterForm(forms.Form):
    PERIOD_CHOICES = [
        ('', 'Todos os períodos'),
        ('today', 'Hoje'),
        ('week', 'Esta semana'),
        ('month', 'Este mês'),
        ('quarter', 'Este trimestre'),
        ('year', 'Este ano'),
    ]

    STATUS_CHOICES = [
        ('', 'Todos os status'),
        ('pending', 'Pendente'),
        ('authorized', 'Autorizado'),
        ('completed', 'Concluído'),
    ]

    search = forms.CharField(
        required=False,
        label='Buscar',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cliente, aparelho, defeito ou OS...'
        })
    )

    client = forms.ModelChoiceField(
        queryset=Person.objects.none(),
        required=False,
        empty_label="Todos os clientes",
        label='Cliente',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    period = forms.ChoiceField(
        choices=PERIOD_CHOICES,
        required=False,
        label='Período',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        label='Status',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    min_value = forms.DecimalField(
        required=False,
        decimal_places=2,
        max_digits=10,
        label='Valor mínimo',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0,00',
            'step': '0.01'
        })
    )

    max_value = forms.DecimalField(
        required=False,
        decimal_places=2,
        max_digits=10,
        label='Valor máximo',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '999999,99',
            'step': '0.01'
        })
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['client'].queryset = Person.objects.filter(
                owner=user, person_type=2
            ).order_by('first_name')
