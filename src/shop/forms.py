from django import forms
from models import Vitrine


class VitrineForm(forms.ModelForm):
    class Meta:
        model = Vitrine
        fields = [
            'nom_boutique',
            'description_boutique',
            'nom_proprietaire',
            'description_proprietaire',
            'horaires',
            'adresse'
        ]
        widgets = {
            'horaires': forms.Textarea(attrs={'placeholder': 'Ex: Lundi: 9h-18h\nMardi: 10h-19h'}),
            'adresse': forms.Textarea(attrs={'placeholder': 'Votre adresse complète'}),
        }