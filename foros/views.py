from django.shortcuts import render


def mostrarIndex(request):
    return render(request, 'index.html')

def mostrarLogin(request):
    return render(request, 'login.html')

def mostrarSignup(request):
    return render(request, 'signup.html')

def mostrarLogout(request):
    pass

def mostrarPerfilUsuario(request):
    return render(request, 'perfil_usuario.html')

def mostrarEditarPerfilUsuario(request):
    return render(request, 'editar_perfil_usuario.html')

def mostrarForo(request):
    return render(request, 'ver_foro.html')

def mostrarCrearComentario(request):
    return render(request, 'crear_comentario.html')

def mostrarEditarComentario(request):
    return render(request, 'editar_comentario.html')

def mostrarAdministrarForos(request):
    return render(request, 'administrar_foros.html')

def mostrarCrearForo(request):
    return render(request, 'crear_foro.html')

def mostrarEditarForo(request):
    return render(request, 'editar_foro.html')

def mostrarAdministrarTematicas(request):
    return render(request, 'administrar_tematicas.html')

def mostrarCrearTematica(request):
    return render(request, 'crear_tematica.html')

def mostrarEditarTematica(request):
    return render(request, 'editar_tematica.html')

def mostrarGestionarUsuarios(request):
    return render(request, 'gestionar_usuarios.html')

def mostrarHistorialAcciones(request):
    return render(request, 'historial_acciones.html')