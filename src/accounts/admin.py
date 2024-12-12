
from django.contrib import admin
from .models import CustomUser
from marketplace.models import Product
from shop.models import Tag
from shop.models import Vitrine

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username','email', 'first_name', 'last_name','role','formatted_date_joined')  # Afficher le champ role
    list_filter = ('role',)  # Filtrer par rôle dans l'admin
    list_editable = ('role',)
    ordering = ('username',)

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'first_name', 'last_name', 'role')
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['role'].choices = CustomUser.ROLE_CHOICES
        return form
    def formatted_date_joined(self, obj):
        # Formater la date dans le format souhaité
        return obj.date_joined.strftime('%d/%m/%Y') if obj.date_joined else '-'

    formatted_date_joined.admin_order_field = 'date_joined'  # Permet de trier par date_joined si nécessaire
    formatted_date_joined.short_description = 'Date d\'inscription'  # Modifier l'intitulé

    def save_model(self, request, obj, form, change):
        role = form.cleaned_data.get('role')
        if role == CustomUser.VENDEUR:
            obj.is_staff = True
            obj.is_admin = False
        elif role == CustomUser.GESTIONNAIRE:
            obj.is_staff = True
            obj.is_admin = True
        else:
            obj.is_staff = False
            obj.is_admin = False

        super().save_model(request, obj, form, change)


admin.site.register(CustomUser, CustomUserAdmin,)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('titre', 'user','vitrine_associée', 'price', 'activate', 'published')
    list_filter = ('activate', 'category', 'published')
    list_editable = ('activate',)  # Permet d'éditer le statut d'activation directement dans la liste
    search_fields = ('titre', 'description', 'user__username')  # Ajoute une barre de recherche
    ordering = ('-published',)  # Trie par date de publication décroissante

    def save_model(self, request, obj, form, change):
        # Ajout d'une vérification pour les administrateurs uniquement
        if request.user.is_superuser:
            super().save_model(request, obj, form, change)

    def vitrine_associée(self, obj):
        """
        Renvoie la vitrine associée au vendeur du produit via user_id.
        """
        try:
            vitrine = Vitrine.objects.get(user=obj.user)
            return vitrine.nom_boutique  # Remplacez 'nom' par le champ correspondant de la vitrine
        except Vitrine.DoesNotExist:
            return "Aucune vitrine"

    vitrine_associée.short_description = "Vitrine associée"

admin.site.register(Product, ProductAdmin)