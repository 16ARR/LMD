from django.db import models

from Blanche import settings


# Create your models here.


class Vitrine(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vitrine',
    )
    nom_boutique = models.CharField(max_length=255)
    description_boutique = models.CharField(max_length=255)
    nom_proprietaire = models.CharField(max_length=255)
    description_proprietaire = models.CharField(max_length=255)
    horaires = models.CharField(max_length=255)  # Clé-valeur pour lundi à dimanche
    adresse = models.CharField(max_length=255)

    def __str__(self):
        return self.nom_boutique