from django.db import models
from django.utils import timezone

# Create your models here.
class Usuario(models.Model):
    TIPO_USUARIO = (
        ('Admin', 'Administrador'),
        ('Normal', 'Usuario Normal'),
    )
    
    ESTADO_CUENTA = (
        ('Activo', 'Activo'),
        ('Suspendido', 'Suspendido'),
        ('Deshabilitado', 'Deshabilitado'),
    )

    rut = models.TextField(max_length=12, unique=True)
    nombres = models.TextField(max_length=100)
    paterno = models.TextField(max_length=50)
    materno = models.TextField(max_length=50, null=True, blank=True)
    correo = models.EmailField(unique=True)
    nacionalidad = models.TextField(max_length=50)
    contraseña = models.TextField(max_length=50)
    tipo_usuario = models.TextField(max_length=10, choices=TIPO_USUARIO, default='Normal')
    estado = models.TextField(max_length=15, choices=ESTADO_CUENTA, default='Activo')
    intentos_fallidos = models.IntegerField(default=0)
    fecha_creacion = models.DateTimeField(default=timezone.now)

class Tematica(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(max_length=400)

class Foro(models.Model):
    nombre = models.TextField(max_length=30, unique=True)
    descripcion = models.TextField(max_length=460)
    imagen = models.ImageField(upload_to='foros/', null=True, blank=True)
    tematica = models.ForeignKey(Tematica, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(default=timezone.now)

class Publicacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    foro = models.ForeignKey(Foro, on_delete=models.CASCADE)
    titulo = models.TextField(max_length=120)
    texto = models.TextField(max_length=5000)
    fecha = models.DateTimeField(default=timezone.now)

class Historial(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    accion = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)

class Palabrotas(models.Model):
    palabra = models.CharField(max_length=100, unique=True)