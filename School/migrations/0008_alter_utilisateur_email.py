# Generated by Django 5.1.7 on 2025-03-17 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('School', '0007_remove_utilisateur_date_inscription_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
