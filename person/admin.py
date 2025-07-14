from django.contrib import admin
from .forms import PersonAdminForm
from .models import Person, Address

# Register your models here.


class PersonAdmin(admin.ModelAdmin):
    form = PersonAdminForm


admin.site.register(Person, PersonAdmin)
admin.site.register(Address)
