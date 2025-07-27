from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .forms import PersonForm
from .models import Person


class PersonListView(LoginRequiredMixin, ListView):
    model = Person
    template_name = 'clients/clients_list.html'

    def get_queryset(self):
        return Person.objects.filter(person_type=2, owner=self.request.user)


def client_create(request):
    if request.method == 'POST':
        client_form = PersonForm(request.POST)
        if client_form.is_valid():
            client = client_form.save(commit=False)
            client.owner = request.user
            client.save()
            return redirect('clients-list')
    else:
        client_form = PersonForm()
    return render(request, 'clients/client_form.html', {
        'client_form': client_form,
    })


def client_edit(request, pk):

    try:
        client = get_object_or_404(Person, pk=pk)

        if request.method == 'POST':
            client_form = PersonForm(request.POST, instance=client)
            if client_form.is_valid():
                client_form.save()
                return redirect('clients-list')
        else:
            client_form = PersonForm(instance=client)

        return render(request, 'clients/client_form.html', {
            'client_form': client_form,
            'object': client,
        })
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise


class ClientDeleteView(DeleteView):
    model = Person
    template_name = 'clients/client_delete.html'
    success_url = reverse_lazy('clients-list')
