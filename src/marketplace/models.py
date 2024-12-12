
from django.core.mail import send_mail

from django.urls import reverse

from django.utils.text import slugify
from django.db import models
from django.template.defaultfilters import slugify

from Blanche import settings
from Blanche.settings import AUTH_USER_MODEL
from accounts.models import CustomUser

# SIZES = [(str(i), str(i)) for i in range(16, 71)]
# YEARS = [(str(y), str(y)) for y in range(1900, timezone.now().year + 1)]
# STATE = [("b", "Bon état"), ("tb", "Très bon état"), ("cn", "Comme neuf")]
# TYPE = [("h", "Homme"), ("f", "Femme"), ("e", "Enfant")]
CATEGORY = [("ch", "Chaussures"), ("pa", "Pantalons"), ("ha", "Hauts")]

def user_directory_path(instance, filename):
    return f"{instance.user.username}/{filename}"

# Create your models here.

class Product(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Vendeur", null=True)
    titre = models.CharField(max_length=50, verbose_name="Titre", help_text="50 caractères max")
    description = models.TextField(max_length=200, verbose_name="Description", help_text="200 caractères max")
    slug = models.SlugField(blank=True)

    price = models.IntegerField(verbose_name="Prix d'achat")
    category = models.CharField(verbose_name="Catégorie", choices=CATEGORY, max_length=20)


    pics_1 = models.ImageField(verbose_name="Photo 1", upload_to=user_directory_path)
    pics_2 = models.ImageField(verbose_name="Photo 2", blank=True, null=True, upload_to=user_directory_path)
    pics_3 = models.ImageField(verbose_name="Photo 3", blank=True, null=True, upload_to=user_directory_path)
    published = models.DateTimeField(verbose_name="Date de publication", auto_now_add=True)
    activate = models.BooleanField(default=False, verbose_name="Activé")


    class Meta:
        verbose_name = "Vêtement"

    def __str__(self):
        return f"{self.user} - {self.get_category_display()} - {self.description}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.description)

        if self._state.adding:
            super().save(*args, **kwargs)
            Product.__send_email()
        else:
            super().save(*args, **kwargs)

    @staticmethod
    def __send_email():
        """
            Sends an email notification about a new announcement.

            This static method sends a predefined email with the subject 'Nouvelle annonce' and a
            message stating 'Nouvelle annonce déposée' to a specified recipient list.

            Note:
            This method is private and intended for internal use within its class.
            """
        send_mail(subject="Nouvelle annonce", message="Nouvelle annonce déposée",
                  recipient_list=["gabrieltrouve5@yahoo.com"], from_email=None)

    def get_absolute_url(self):
        # https://docs.djangoproject.com/fr/4.2/ref/models/instances/#get-absolute-url
        return reverse(viewname="shop:detail", kwargs={"slug": self.slug, "pk": self.pk})

    @property
    def garment_year(self):
        return self.year or "NC"