# Generated by Django 5.0 on 2024-10-31 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foros', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='tematicas',
            field=models.ManyToManyField(blank=True, to='foros.tematica'),
        ),
    ]