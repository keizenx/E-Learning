# Generated by Django 5.1.7 on 2025-03-17 03:46

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('School', '0006_update_models_with_defaults'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='utilisateur',
            name='date_inscription',
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='is_approved',
            field=models.BooleanField(default=False, help_text="Indique si l'enseignant a été approuvé par un administrateur"),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='nom',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'Administrateur'), ('TEACHER', 'Enseignant'), ('STUDENT', 'Étudiant'), ('ACADEMIC', 'Responsable académique')], default='STUDENT', max_length=10),
        ),
    ]
