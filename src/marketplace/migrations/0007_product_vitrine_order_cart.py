# Generated by Django 5.1.2 on 2024-12-17 13:32

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0006_alter_product_activate_alter_product_category'),
        ('shop', '0008_remove_vitrine_proprietaire'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='vitrine',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.vitrine'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantité')),
                ('reference', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Référence')),
                ('ordered', models.BooleanField(default=False, verbose_name='Commandée')),
                ('ordered_date', models.DateTimeField(blank=True, null=True, verbose_name='Date de commande')),
                ('validation', models.BooleanField(default=False, verbose_name='Validation de la commande')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='marketplace.product', verbose_name='Produit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
            options={
                'verbose_name': 'Commande',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantité')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
                ('orders', models.ManyToManyField(to='marketplace.order', verbose_name='Commandes')),
            ],
            options={
                'verbose_name': 'Panier',
            },
        ),
    ]