# Generated by Django 5.0 on 2024-11-01 00:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foros', '0002_usuario_tematicas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='tematicas',
        ),
    ]