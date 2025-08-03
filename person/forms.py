from django import forms
from .models import Person


class PersonCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput)

    class Meta:
        model = Person
        fields = ('username', 'first_name', 'last_name', 'email', 'person_type', 'phone')

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("As senhas não conferem")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'email', 'phone']

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone', '')
        if phone and len(phone) < 10:
            self.add_error('phone', 'Informe um telefone válido.')
        return cleaned_data

    def generate_username(self, first_name, last_name, phone):
        username_base = f"{first_name.strip()}{last_name.strip()}".lower()
        digits = ''.join(filter(str.isdigit, phone))
        suffix = digits[-4:] if len(digits) >= 4 else digits
        username = username_base + suffix

        unique_username = username
        counter = 1
        while Person.objects.filter(username=unique_username).exists():
            unique_username = f"{username}{counter}"
            counter += 1

        return unique_username

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.person_type = 2

        first_name = self.cleaned_data.get('first_name', '')
        last_name = self.cleaned_data.get('last_name', '')
        phone = self.cleaned_data.get('phone', '')

        username = self.generate_username(first_name, last_name, phone)
        instance.username = username

        if commit:
            instance.save()
        return instance
