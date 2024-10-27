# Generated by Django 5.0 on 2024-10-27 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foros', '0002_rename_post_publicacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foro',
            name='imagen_url',
        ),
        migrations.AddField(
            model_name='foro',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='foros/'),
        ),
    ]
