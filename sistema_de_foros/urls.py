from django.contrib import admin
from django.urls import path
from foros import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.mostrarIndex, name='index'),
    path('login/', views.mostrarLogin, name='login'),
    path('logout/', views.mostrarLogout, name='logout'),
    path('signup/', views.mostrarSignup, name='signup'),
    path('perfil_usuario/', views.mostrarPerfilUsuario, name='perfil_usuario'),
    path('editar_usuario/', views.mostrarEditarPerfilUsuario, name='editar_usuario'),
    path('foro/', views.mostrarForo, name='foro'),
    path('foro/crear_comentario/', views.mostrarCrearComentario, name='crear_comentario'),
    path('foro/editar_comentario/', views.mostrarEditarComentario, name='editar_comentario'),
    path('administrar_foros/', views.mostrarAdministrarForos, name='administrar_foros'),
    path('crear_foro/', views.mostrarCrearForo, name='crear_foro'),
    path('editar_foro/', views.mostrarEditarForo, name='editar_foro'),
    path('administrar_tematicas/', views.mostrarAdministrarTematicas, name='administrar_tematicas'),
    path('crear_tematica/', views.mostrarCrearTematica, name='crear_tematica'),
    path('editar_tematica/', views.mostrarEditarTematica, name='editar_tematica'),
    path('gestionar_usuarios/', views.mostrarGestionarUsuarios, name='gestionar_usuarios'),
    path('historial_acciones/', views.mostrarHistorialAcciones, name='historial_acciones'),
]
