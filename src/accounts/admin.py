
from django.contrib import admin
from .models import CustomUser
from shop.models import Tag # Assurez-vous de l'importer correctement

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