# Generated by Django 5.1.2 on 2024-12-17 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0008_alter_product_category_alter_product_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('ch', 'Chaussures'), ('pa', 'Pantalons'), ('ha', 'Hauts'), ('my', 'Mythique')], max_length=20, verbose_name='Catégorie'),
        ),
    ]