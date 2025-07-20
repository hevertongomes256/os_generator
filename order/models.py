from django.db import models
from person.models import Person


class Order(models.Model):

    client = models.ForeignKey(Person, verbose_name='Cliente', on_delete=models.CASCADE, related_name='person_order')
    device = models.CharField(verbose_name='Aparelho', max_length=255)
    defect = models.CharField(verbose_name='Defeito', max_length=255)
    additional_info = models.TextField(verbose_name='Observações', null=True, blank=True)
    additional_info_exit = models.TextField(null=True, blank=True)
    additional_description = models.TextField(verbose_name='Serviço Prestado')
    service_autorized = models.BooleanField(verbose_name='Serviço Autorizado', default=False)
    service_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor Total'
    )
    service_initial = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor de Entrada',
        null=True,
        blank=True
    )
    missing_payment = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor a receber',
        null=True,
        blank=True
    )
    shipping_date = models.DateTimeField(verbose_name='Data de recebimento', auto_now_add=True, null=True, blank=True)
    name_withdrawal = models.CharField(verbose_name='Nome de quem retirou', max_length=255, null=True, blank=True)
    withdrawal_date = models.DateTimeField(verbose_name='Data de retirada', null=True, blank=True)

    def __str__(self):
        return f'{self.id}'


class Checklist(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='checklist')

    def __str__(self):
        return f'{self.id}'


class ChecklistItem(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=255)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}'
