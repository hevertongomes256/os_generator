from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Person


class PersonListView(LoginRequiredMixin, ListView):
    model = Person
    template_name = 'clients/clients-list.html'

    def get_queryset(self):
        return Person.objects.filter(person_type=2)
