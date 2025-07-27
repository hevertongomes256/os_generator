from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import PersonCreateForm, PersonChangeForm
from .models import Person, Address

# Register your models here.


class PersonAdmin(UserAdmin):
    add_form = PersonCreateForm
    form = PersonChangeForm
    model = Person
    list_display = ('username', 'email', 'first_name', 'last_name', 'person_type', 'has_usable_password_display')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'first_name', 'last_name', 'person_type',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'first_name', 'last_name', 'person_type', 'owner',)}),
    )

    def has_usable_password_display(self, obj):
        return obj.has_usable_password()
    has_usable_password_display.boolean = True
    has_usable_password_display.short_description = 'Senha configurada?'


admin.site.register(Person, PersonAdmin)
admin.site.register(Address)
