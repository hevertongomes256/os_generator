from django.db import models
from person.models import Person


class Order(models.Model):

    client = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='person_order')
    device = models.CharField(verbose_name='Aparelho', max_length=255)
    defect = models.CharField(verbose_name='Defeito', max_length=255)
    additional_info = models.TextField(null=True, blank=True)
    additional_info_exit = models.TextField(null=True, blank=True)
    additional_description = models.TextField()
    service_autorized = models.BooleanField(default=False)
    service_total = models.DecimalField(
        max_digits=10,  
        decimal_places=2,
        verbose_name='Valor Total'
    )
    service_initial = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor Total',
        null=True,
        blank=True
    )
    missing_payment = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor Total',
        null=True,
        blank=True
    )
    shipping_date = models.DateTimeField(null=True, blank=True)
    name_withdrawal = models.CharField(verbose_name='Defeito', max_length=255)
    withdrawal_date = models.DateTimeField(null=True, blank=True)


class Checklist(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='checklist')


class ChecklistItem(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=255)
    checked = models.BooleanField(default=False)
