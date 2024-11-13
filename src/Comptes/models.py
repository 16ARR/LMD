from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save

# Choices pour le type d'utilisateur
TYPE_USER = [("h", "Homme"), ("f", "Femme"), ("nr", "Non renseigné")]


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, date_of_birth, phone_number, password=None):
        if not email:
            raise ValueError("L'utilisateur doit avoir une adresse email")

        # Crée un utilisateur avec les informations fournies
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, date_of_birth, phone_number, password):
        # Crée un super-utilisateur avec les droits administratifs
        user = self.create_user(
            email,
            username,
            first_name,
            last_name,
            date_of_birth,
            phone_number,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True  # Nécessaire pour l'accès au site d'administration
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True, default="")
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30, default='')
    date_of_birth = models.DateField(null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    type = models.CharField(max_length=10, verbose_name="Sexe", choices=TYPE_USER)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'date_of_birth', 'phone_number']

    objects = MyUserManager()

    def has_perm(self, perm, obj=None):
        # Tous les utilisateurs peuvent avoir des permissions s'ils sont actifs
        return True

    def has_module_perms(self, app_label):
        # L'utilisateur a accès aux modules s'il est actif
        return True

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Définition des rôles de l'utilisateur
    CLIENT = 'client'
    VENDEUR = 'vendeur'
    GESTIONNAIRE = 'gestionnaire'

    ROLE_CHOICES = [
        (CLIENT, 'Client'),
        (VENDEUR, 'Vendeur'),
        (GESTIONNAIRE, 'Gestionnaire de vendeur'),
    ]

    # Champ pour stocker le rôle
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default=CLIENT)

    class Meta:
        verbose_name = 'Utilisateur'

    def __str__(self):
        # Utilise l'email de l'utilisateur pour représenter le profil
        return f"{self.user.first_name} - {self.get_role_display()}"


# Signal pour créer un profil automatiquement quand un utilisateur est créé
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=settings.AUTH_USER_MODEL)
