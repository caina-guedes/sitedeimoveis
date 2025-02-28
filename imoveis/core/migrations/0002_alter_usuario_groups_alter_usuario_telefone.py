# Generated by Django 5.1.6 on 2025-02-22 18:44

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='usuario_groups', to='auth.group'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='telefone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region='BR'),
        ),
    ]
