from django.db import models
from django.utils.text import slugify
from Blanche import settings


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Vitrine(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vitrine',
    )
    nom_boutique = models.CharField(max_length=255)
    slug_vitrine = models.SlugField(max_length=255, unique=True, blank=True)
    description_boutique = models.TextField()
    nom_proprietaire = models.CharField(max_length=255)
    description_proprietaire = models.TextField()
    # horaires = models.CharField(max_length=255)  # Clé-valeur pour lundi à dimanche
    adresse = models.CharField(max_length=255)
    tags=models.ManyToManyField(Tag, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug_vitrine:
            self.slug = slugify(self.nom_boutique)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom_boutique



