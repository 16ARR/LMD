# Generated by Django 5.1.2 on 2024-12-06 13:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_vitrine_slug_vitrine'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='vitrine',
            name='proprietaire',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='vitrines', to=settings.AUTH_USER_MODEL),
        ),
    ]