from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

# Create your models here.
TYPE_USER = [("h", "Homme"), ("f", "Femme"), ("nr", "Non renseigné")]

class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        unique=True,
        max_length=255,
        blank=False,
    )
    type = models.CharField(max_length=10, verbose_name="Sexe", choices=TYPE_USER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
