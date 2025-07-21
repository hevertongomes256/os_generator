from django import forms
from .models import Person


class PersonAdminForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['username', 'first_name', 'last_name', 'email', 'person_type', 'phone']

    def clean(self):
        cleaned_data = super().clean()
        person_type = cleaned_data.get('person_type')
        password = cleaned_data.get('password')
        if person_type == 'logista' and not password:
            raise forms.ValidationError("Logista precisa de senha.")
        return cleaned_data


class PersonForm(forms.ModelForm):
    model = Person
    fields = ['first_name', 'last_name', 'email', 'phone']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.person_type = 2
        if commit:
            instance.save()
        return instance
