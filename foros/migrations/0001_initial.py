# Generated by Django 5.0 on 2024-11-02 21:22

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Foro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(max_length=30, unique=True)),
                ('descripcion', models.TextField(max_length=460)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='foros/')),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Palabrotas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('palabra', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tematica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('descripcion', models.TextField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=12, unique=True)),
                ('nombres', models.TextField(max_length=100)),
                ('paterno', models.TextField(max_length=50)),
                ('materno', models.TextField(blank=True, max_length=50, null=True)),
                ('correo', models.EmailField(max_length=254, unique=True)),
                ('nacionalidad', models.TextField(max_length=50)),
                ('contraseña', models.TextField(max_length=50)),
                ('tipo_usuario', models.TextField(choices=[('Admin', 'Administrador'), ('Normal', 'Usuario Normal')], default='Normal', max_length=10)),
                ('estado', models.TextField(choices=[('Activo', 'Activo'), ('Suspendido', 'Suspendido'), ('Deshabilitado', 'Deshabilitado')], default='Activo', max_length=15)),
                ('intentos_fallidos', models.IntegerField(default=0)),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Publicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.TextField(max_length=120)),
                ('texto', models.TextField(max_length=5000)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('foro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foros.foro')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foros.usuario')),
            ],
        ),
        migrations.AddField(
            model_name='foro',
            name='tematica',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foros.tematica'),
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(max_length=1000)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('publicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foros.publicacion')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foros.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Historial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accion', models.TextField()),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foros.usuario')),
            ],
        ),
    ]
