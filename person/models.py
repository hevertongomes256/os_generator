from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class Person(AbstractUser):

    STORE_OWNER = 1
    CLIENT = 2
    PERSON_TYPE_CHOICES = (
        (STORE_OWNER, 'Logista'),
        (CLIENT, 'Cliente')
    )
    person_type = models.PositiveSmallIntegerField(choices=PERSON_TYPE_CHOICES, default=STORE_OWNER)
    phone = models.CharField(max_length=20, blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='users_created'
    )

    def __str__(self):
        return f'{self.username}'


class Address(models.Model):
    client = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='person_address')
    street = models.CharField(verbose_name='Rua', max_length=255)
    number = models.CharField(verbose_name='Número', max_length=10)
    complement = models.CharField(verbose_name='Complemento', max_length=100, blank=True, null=True)
    neighbood = models.CharField(verbose_name='Bairro', max_length=100, blank=True, null=True)
    city = models.CharField(verbose_name='Cidade', max_length=100)
    state = models.CharField(verbose_name='Estado', max_length=2)
    cep = models.CharField(verbose_name='CEP', max_length=10)

    def __str__(self):
        return f'{self.cep}'
