from django.contrib import admin
from django.urls import path
from foros import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.mostrarIndex),
    path('login/', views.mostrarLogin),
    path('logout/', views.mostrarLogout),
    path('signup/', views.mostrarSignup),
    path('perfil_usuario/', views.mostrarPerfilUsuario),
    path('editar_usuario/', views.mostrarEditarPerfilUsuario),
    path('foro/', views.mostrarForo),
    path('foro/crear_comentario/', views.mostrarCrearComentario),
    path('foro/editar_comentario/', views.mostrarEditarComentario),
    path('administrar_foros/', views.mostrarAdministrarForos),
    path('crear_foro/', views.mostrarCrearForo),
    path('editar_foro/', views.mostrarEditarForo),
    path('administrar_tematicas/', views.mostrarAdministrarTematicas),
    path('crear_tematica/', views.mostrarCrearTematica),
    path('editar_tematica/', views.mostrarEditarTematica),
    path('gestionar_usuarios/', views.mostrarGestionarUsuarios),
    path('historial_acciones/', views.mostrarHistorialAcciones),
]
