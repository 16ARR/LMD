from django.conf import settings
from django.contrib.auth import user_logged_in
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save

# Create your models here.
TYPE_USER = [("h", "Homme"), ("f", "Femme"), ("nr", "Non renseigné")]


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, date_of_birth, phone_number, password=None):
        if not email:
            raise ValueError("L'utilisateur doit avoir une adresse email")
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
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True, default="")
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30, default='')
    date_of_birth = models.DateField(null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=True )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    type = models.CharField(max_length=10, verbose_name="Sexe", choices=TYPE_USER)

    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


def post_save_receiver(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(post_save_receiver, sender=settings.AUTH_USER_MODEL)