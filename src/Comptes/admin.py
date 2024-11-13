from django.contrib import admin

from .models import Profile, CustomUser



@admin.register(CustomUser)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "phone_number")

