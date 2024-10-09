# Generated by Django 4.2 on 2024-10-07 20:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('foros', '0002_remove_comentario_foro_remove_comentario_usuario_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Foro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(max_length=30)),
                ('descripcion', models.TextField(max_length=460)),
                ('imagen_url', models.URLField(blank=True, null=True)),
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
                ('rut', models.TextField(max_length=12, unique=True)),
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
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.TextField(max_length=120)),
                ('texto', models.TextField(max_length=5000)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('foro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foros.foro')),
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
        migrations.AddField(
            model_name='foro',
            name='tematicas',
            field=models.ManyToManyField(related_name='foros', to='foros.tematica'),
        ),
    ]
