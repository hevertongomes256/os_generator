from django.contrib import admin
from .models import Person, Address
from .forms import PersonCreationForm

# Register your models here.


class PersonAdmin(admin.ModelAdmin):
    form = PersonCreationForm


admin.site.register(Person, PersonAdmin)
admin.site.register(Address)
