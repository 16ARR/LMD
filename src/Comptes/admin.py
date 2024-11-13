from django.contrib import admin

from .models import Profile



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "get_username", "get_first_name")

    # Crée des méthodes pour accéder aux champs du modèle CustomUser lié
    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = 'Username'  # Définit un label pour l’affichage

    def get_first_name(self, obj):
        return obj.user.first_name

    get_first_name.short_description = 'First Name'