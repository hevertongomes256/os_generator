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
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Person.objects.filter(person_type=2)


ChecklistItemFormSet = inlineformset_factory(
    Checklist,
    ChecklistItem,
    fields=['description', 'checked'],
    extra=len(initial_data_checklist),
    can_delete=False
)
