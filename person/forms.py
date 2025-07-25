from django import forms
from .models import Person
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class PersonCreateForm(UserCreationForm):
    class Meta:
        model = Person
        fields = ['username', 'email', 'first_name', 'last_name', 'person_type']

    def clean(self):
        cleaned_data = super().clean()
        person_type = cleaned_data.get('person_type')
        password = cleaned_data.get('password')
        if person_type == 'logista' and not password:
            raise forms.ValidationError("Logista precisa de senha.")
        return cleaned_data


class PersonChangeForm(UserChangeForm):
    class Meta:
        model = Person
        fields = ['username', 'email', 'first_name', 'last_name', 'person_type']


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'email', 'phone']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.person_type = 2
        if commit:
            instance.save()
        return instance
