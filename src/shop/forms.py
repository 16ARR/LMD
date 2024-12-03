from django import forms
from shop.models import Vitrine, Tag


class VitrineForm(forms.ModelForm):
    class Meta:
        model = Vitrine
        fields = [
            'nom_boutique',
            'description_boutique',
            'nom_proprietaire',
            'description_proprietaire',
            # 'horaires',
            'adresse',
            'tags'
            ]
        tags = forms.ModelMultipleChoiceField(
            queryset=Tag.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=False
        )

class VitrineEditForm(forms.ModelForm):
    class Meta:
        model = Vitrine
        fields = ['nom_boutique', 'description_boutique', 'nom_proprietaire', 'description_proprietaire', 'adresse', 'tags']

        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)



        # widgets = {
        #     'horaires': forms.Textarea(attrs={'placeholder': 'Ex: Lundi: 9h-18h\nMardi: 10h-19h'}),
        #     'adresse': forms.Textarea(attrs={'placeholder': 'Votre adresse complète'}),
        # }

