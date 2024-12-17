from django.core.mail import send_mail
from django.urls import reverse
from django.utils.text import slugify
from django.db import models
from Blanche.settings import AUTH_USER_MODEL

CATEGORY = [("ch", "Chaussures"), ("pa", "Pantalons"), ("ha", "Hauts"),("my","Mythique")]

def user_directory_path(instance, filename):
    return f"{instance.user.username}/{filename}"

class Product(models.Model):
    titre = models.CharField(max_length=50, verbose_name="Titre", help_text="50 caractères max")
    description = models.TextField(max_length=200, verbose_name="Description", help_text="200 caractères max")
    slug = models.SlugField(blank=True, unique=True)
    user = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="product",
        null=True
    )
    price = models.IntegerField(verbose_name="Prix d'achat")
    category = models.CharField(verbose_name="Catégorie", choices=CATEGORY, max_length=20)
    pics_1 = models.ImageField(verbose_name="Photo 1", upload_to=user_directory_path)
    pics_2 = models.ImageField(verbose_name="Photo 2", blank=True, null=True, upload_to=user_directory_path)
    pics_3 = models.ImageField(verbose_name="Photo 3", blank=True, null=True, upload_to=user_directory_path)
    published = models.DateTimeField(verbose_name="Date de publication", auto_now_add=True)
    activate = models.BooleanField(default=True, verbose_name="Activé")

    class Meta:
        verbose_name = "Article"

    def __str__(self):
        return f"{self.user} - {self.get_category_display()} - {self.description}"

    def save(self, *args, **kwargs):
        # Générer un slug unique
        if not self.slug:
            base_slug = slugify(self.titre)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        is_new = self._state.adding  # Vérifie si l'objet est nouveau
        super().save(*args, **kwargs)

        # Envoi de l'email après création
        if is_new:
            self.__send_email()

    @staticmethod
    def __send_email():
        """
        Envoie une notification par email lorsqu'un nouveau produit est ajouté.
        """
        send_mail(
            subject="Nouvelle annonce",
            message="Nouvelle annonce déposée",
            recipient_list=["gabrieltrouve5@yahoo.com"],
            from_email=None
        )

    def get_absolute_url(self):
        """
        Retourne l'URL absolue du produit.
        """
        return reverse("shop:detail", kwargs={"slug": self.slug, "pk": self.pk})
