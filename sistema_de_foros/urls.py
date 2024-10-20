from django.contrib import admin
from django.urls import path
from foros import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.mostrarIndex, name='index'),
    path('login/', views.mostrarLogin, name='login'),
    path('form_login/', views.formLogin, name='form_login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.mostrarSignup, name='signup'),
    path('form_signup/', views.formSignup, name='form_signup'),
    path('perfil_usuario/<int:id>/', views.mostrarPerfilUsuario, name='perfil_usuario'),
    path('editar_usuario/<int:id>', views.mostrarEditarPerfilUsuario, name='editar_usuario'),
    path('form_editar_usuario/<int:id>', views.formEditarPerfilUsuario, name='form_editar_usuario'),
    path('administrar_tematicas/', views.mostrarAdministrarTematicas, name='administrar_tematicas'),
    path('crear_tematica/', views.mostrarCrearTematica, name='crear_tematica'),
    path('form_crear_tematica/', views.formCrearTematica, name='form_crear_tematica'),
    path('editar_tematica/<int:id>', views.mostrarEditarTematica, name='editar_tematica'),
    path('form_editar_tematica/<int:id>', views.formEditarTematica, name='form_editar_tematica'),
    path('foro/', views.mostrarForo, name='foro'),
    path('crear_foro/', views.mostrarCrearForo, name='crear_foro'),
    path('form_crear_foro/', views.formCrearForo, name='form_crear_foro'),
    path('editar_foro/<int:id>', views.mostrarEditarForo, name='editar_foro'),
    path('form_editar_foro/<int:id>', views.formEditarForo, name='form_editar_foro'),
    path('foro/crear_comentario/', views.mostrarCrearComentario, name='crear_comentario'),
    path('foro/editar_comentario/', views.mostrarEditarComentario, name='editar_comentario'),
    path('administrar_foros/', views.mostrarAdministrarForos, name='administrar_foros'),
    path('gestionar_usuarios/', views.mostrarGestionarUsuarios, name='gestionar_usuarios'),
    path('historial_acciones/', views.mostrarHistorialAcciones, name='historial_acciones'),
]
