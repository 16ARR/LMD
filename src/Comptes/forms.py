from django import forms
from django.forms.widgets import DateInput
from .models import CustomUser
import re

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=3)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'date_of_birth', 'phone_number', 'password']
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date', 'placeholder': 'DD-MM-YYYY'}),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 3 or not re.search(r'\d', password) or not re.search(r'[A-Za-z]', password):
            raise forms.ValidationError(
                "Le mot de passe doit contenir au moins 3 caractères, dont au moins un chiffre et une lettre."
            )
        return password

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth and date_of_birth.year < 1900:
            raise forms.ValidationError("L'année de naissance doit être postérieure ou égale à 1900.")
        return date_of_birth

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Les mots de passe ne correspondent pas.")

class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'date_of_birth', 'phone_number']
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date', 'placeholder': 'DD-MM-YYYY'}),
        }
