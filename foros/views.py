from django.shortcuts import render, redirect, get_object_or_404
from functools import wraps
from datetime import datetime
from .models import Usuario, Tematica, Foro, Publicacion, Historial, Respuesta, Palabrotas

# Decoradores
def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('estadoSesion'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('estadoSesion'):
            return redirect('login')
        if request.session.get('tipUsuario') != 'Admin':
            return redirect('acceso_denegado')
        return view_func(request, *args, **kwargs)
    return wrapper

# Utilidades
def get_session_data(request):
    return {
        'idUsuario': request.session.get("idUsuario"),
        'nomUsuario': request.session.get("nomUsuario"),
        'tipUsuario': request.session.get("tipUsuario"),
    }

def registrar_historial(accion, usuario_id):
    Historial.objects.create(accion=accion, fecha=datetime.now(), usuario_id=usuario_id)

def verificar_si_existe(clase, campo, valor):
    return clase.objects.filter(**{campo: valor}).exists()

def obtener_usuario(request):
    usuario_id = request.session.get("idUsuario")
    return get_object_or_404(Usuario, id=usuario_id)

# Views
@login_required
def mostrarIndex(request):
    return render(request, 'index.html', get_session_data(request))

def mostrarLogin(request):
    return render(request, 'login.html')

def formLogin(request):
    rut = request.POST.get("txtrut")
    pas = request.POST.get("txtpas")

    try:
        usuario = Usuario.objects.get(rut=rut)
    except Usuario.DoesNotExist:
        return render(request, 'login.html', {'mensaje_error': 'Usuario no encontrado.'})

    if usuario.estado == 'Suspendido':
        return render(request, 'login.html', {'mensaje_error': 'Su cuenta está suspendida. Contacte al administrador.'})

    if usuario.contraseña == pas:
        usuario.intentos_fallidos = 0
        usuario.save()

        request.session["estadoSesion"] = True
        request.session["idUsuario"] = usuario.id
        request.session["nomUsuario"] = usuario.nombres  
        request.session["tipUsuario"] = usuario.tipo_usuario

        registrar_historial("Inicia sesión", usuario.id)

        return redirect('index')
    else:
        usuario.intentos_fallidos += 1
        usuario.save()

        if usuario.intentos_fallidos >= 3:
            usuario.estado = 'Suspendido'
            usuario.save()
            mensaje_error = 'Su cuenta ha sido suspendida por múltiples intentos fallidos.'
        else:
            intentos_restantes = 3 - usuario.intentos_fallidos
            mensaje_error = f'Contraseña incorrecta. Intentos restantes: {intentos_restantes}'

        return render(request, 'login.html', {'mensaje_error': mensaje_error})

def mostrarSignup(request):
    return render(request, 'signup.html')

def formSignup(request):
    rut_usu = request.POST.get('txtrut')
    nom_usu = request.POST.get('txtnom')
    apem_usu = request.POST.get('txtapem')
    apep_usu = request.POST.get('txtapep')
    ema_usu = request.POST.get('txtema')
    nac_usu = request.POST.get('txtnac')
    pas_usu = request.POST.get('txtpas')
    pas2_usu = request.POST.get('txtpas2')
    
    errores = {}

    if pas_usu != pas2_usu:
        errores['contraseña'] = 'Las contraseñas no coinciden.'
        
    if verificar_si_existe(Usuario, 'rut', rut_usu):
        errores['rut'] = f'El rut: {rut_usu} ya existe.'
    
    if verificar_si_existe(Usuario, 'correo', ema_usu):
        errores['correo'] = f'El correo: {ema_usu} ya existe.'
        
    if errores:
        return render(request, 'signup.html', {'errores': errores})

    try:
        usuario = Usuario.objects.create(
            rut=rut_usu,
            nombres=nom_usu,
            paterno=apem_usu,
            materno=apep_usu,
            correo=ema_usu,
            nacionalidad=nac_usu,
            contraseña=pas_usu
        )
        
        registrar_historial("Registro de usuario", usuario.id)

        return redirect('login')
        
    except Exception as e:
        errores['db_error'] = f'Error al crear el usuario: {str(e)}'
        return render(request, 'signup.html', {'errores': errores})

def logout(request):
    registrar_historial("Cierre sesión", request.session.get("idUsuario"))
    request.session.flush()
    return redirect('login')

@login_required
def mostrarPerfilUsuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    datos = {'usuario': usuario}
    datos.update(get_session_data(request))
    return render(request, 'perfil_usuario.html', datos)

@login_required
def mostrarEditarPerfilUsuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    idUsuario = request.session.get("idUsuario")
    tipUsuario = request.session.get("tipUsuario")

    if tipUsuario != 'Admin' and idUsuario != usuario.id:
        return redirect('acceso_denegado')

    datos = {'usuario': usuario}
    datos.update(get_session_data(request))
    return render(request, 'editar_perfil_usuario.html', datos)

@login_required
def formEditarPerfilUsuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    idUsuario = request.session.get("idUsuario")
    tipUsuario = request.session.get("tipUsuario")

    if tipUsuario != 'Admin' and idUsuario != usuario.id:
        return redirect('acceso_denegado')

    nom_usu = request.POST.get('txtnom')
    apem_usu = request.POST.get('txtapem')
    apep_usu = request.POST.get('txtapep')
    nac_usu = request.POST.get('txtnac')
    pas_usu = request.POST.get('txtpas')
    pas2_usu = request.POST.get('txtpas2')

    errores = {}

    if pas_usu != pas2_usu:
        errores['contraseña'] = 'Las contraseñas no coinciden.'
        datos = {'errores': errores, 'usuario': usuario}
        datos.update(get_session_data(request))
        return render(request, 'editar_perfil_usuario.html', datos)

    try:
        usuario.nombres = nom_usu
        usuario.materno = apem_usu
        usuario.paterno = apep_usu
        usuario.nacionalidad = nac_usu
        usuario.contraseña = pas_usu
        usuario.save()
        
        registrar_historial("Edición perfil", idUsuario)

        return redirect('perfil_usuario', id=usuario.id)
    except Exception as e:
        errores['db_error'] = f'Error al actualizar el usuario: {str(e)}'
        datos = {'errores': errores, 'usuario': usuario}
        datos.update(get_session_data(request))
        return render(request, 'editar_perfil_usuario.html', datos)
        
@admin_required
def mostrarGestionarUsuarios(request):
    usuarios = Usuario.objects.all()
    datos = {'usuarios': usuarios}
    datos.update(get_session_data(request))
    return render(request, 'gestionar_usuarios.html', datos)

@admin_required
def mostrarCrearTematica(request):
    return render(request, 'crear_tematica.html')

@admin_required
def formCrearTematica(request):
    nom_tematica = request.POST.get('txtnomtem')
    des_tematica = request.POST.get('txtdestem')
    
    errores = {}

    if verificar_si_existe(Tematica, 'nombre', nom_tematica):
        errores['nombre'] = f'La temática: {nom_tematica} ya existe.'

    if errores:
        return render(request, 'crear_tematica.html', {'errores': errores})
    
    try:
        tematica = Tematica.objects.create(nombre=nom_tematica, descripcion=des_tematica)
        
        registrar_historial("Creación de temática", request.session.get("idUsuario"))

        return redirect('administrar_tematicas')
    
    except Exception as e:
        errores['db_error'] = f'Error al crear la temática: {str(e)}'
        return render(request, 'crear_tematica.html', {'errores': errores})

@admin_required
def mostrarEditarTematica(request, id):
    tematica = get_object_or_404(Tematica, id=id)
    return render(request, 'editar_tematica.html', {'tematica': tematica})

@admin_required
def formEditarTematica(request, id):
    nom_tematica = request.POST.get('txtnomtem')
    des_tematica = request.POST.get('txtdestem')
    
    errores = {}

    if Tematica.objects.filter(nombre=nom_tematica).exclude(id=id).exists():
        errores['nombre'] = f'La temática: {nom_tematica} ya existe.'

    tematica = get_object_or_404(Tematica, id=id)

    if errores:
        return render(request, 'editar_tematica.html', {'errores': errores, 'tematica': tematica})
    
    try:
        tematica.nombre = nom_tematica
        tematica.descripcion = des_tematica
        tematica.save()
        
        registrar_historial("Edición de temática", request.session.get("idUsuario"))

        return redirect('administrar_tematicas')
    
    except Exception as e:
        errores['db_error'] = f'Error al editar la temática: {str(e)}'
        return render(request, 'editar_tematica.html', {'errores': errores, 'tematica': tematica})

@admin_required
def eliminarTematica(request, id):
    tematica = get_object_or_404(Tematica, id=id)
    try:
        tematica.delete()
        registrar_historial("Eliminación temática", request.session.get("idUsuario"))
    except Exception as e:
        errores = {'db_error': f'Error al eliminar la temática: {str(e)}'}
        tematicas = Tematica.objects.all()
        datos = {'errores': errores, 'tematicas': tematicas}
        datos.update(get_session_data(request))
        return render(request, 'administrar_tematicas.html', datos)
    return redirect('administrar_tematicas')

@admin_required
def mostrarAdministrarTematicas(request):
    tematicas = Tematica.objects.all()
    datos = {'tematicas': tematicas}
    datos.update(get_session_data(request))
    return render(request, 'administrar_tematicas.html', datos)

@login_required
def mostrarForo(request, foro_id):
    foro = get_object_or_404(Foro, id=foro_id)
    publicaciones = Publicacion.objects.filter(foro=foro)
    datos = {'foro': foro, 'publicaciones': publicaciones}
    datos.update(get_session_data(request))
    return render(request, 'ver_foro.html', datos)

@admin_required
def mostrarCrearForo(request):
    tematicas = Tematica.objects.all()
    return render(request, 'crear_foro.html', {'tematicas': tematicas})

@admin_required
def formCrearForo(request):
    nom_foro = request.POST.get('txtnomfor')
    des_foro = request.POST.get('txtdesfor')
    tema_id = request.POST.get('cbotem')
    imagen = request.FILES.get('imagen')
    
    errores = {}

    if verificar_si_existe(Foro, 'nombre', nom_foro):
        errores['nombre'] = f'El foro: {nom_foro} ya existe, intente con otro nombre.'

    if errores:
        tematicas = Tematica.objects.all()
        return render(request, 'crear_foro.html', {'errores': errores, 'tematicas': tematicas})

    try:
        tematica = get_object_or_404(Tematica, id=tema_id)
        foro = Foro(nombre=nom_foro, descripcion=des_foro, tematica=tematica)
        if imagen:
            foro.imagen = imagen
        foro.save()
        
        registrar_historial("Creación de foro", request.session.get("idUsuario"))

        return redirect('administrar_foros')
    
    except Exception as e:
        errores['db_error'] = f'Error al crear el foro: {str(e)}'
        tematicas = Tematica.objects.all()
        return render(request, 'crear_foro.html', {'errores': errores, 'tematicas': tematicas})

@admin_required
def mostrarEditarForo(request, id):
    foro = get_object_or_404(Foro, id=id)
    tematicas = Tematica.objects.all()
    return render(request, 'editar_foro.html', {'foro': foro, 'tematicas': tematicas})

@admin_required
def formEditarForo(request, id):
    nom_foro = request.POST.get('txtnomfor')
    des_foro = request.POST.get('txtdesfor')
    tema_id = request.POST.get('cbotem')
    imagen = request.FILES.get('imagen')

    errores = {}

    if Foro.objects.filter(nombre=nom_foro).exclude(id=id).exists():
        errores['nombre'] = f'El foro: {nom_foro} ya existe, intente con otro nombre.'

    foro = get_object_or_404(Foro, id=id)
    tematica = get_object_or_404(Tematica, id=tema_id)

    if errores:
        tematicas = Tematica.objects.all()
        return render(request, 'editar_foro.html', {'errores': errores, 'foro': foro, 'tematicas': tematicas})

    try:
        foro.nombre = nom_foro
        foro.descripcion = des_foro
        foro.tematica = tematica
        if imagen:
            foro.imagen = imagen
        foro.save()
        
        registrar_historial("Edición foro", request.session.get("idUsuario"))

        return redirect('administrar_foros')
    
    except Exception as e:
        errores['db_error'] = f'Error al editar el foro: {str(e)}'
        tematicas = Tematica.objects.all()
        return render(request, 'editar_foro.html', {'errores': errores, 'foro': foro, 'tematicas': tematicas})

@admin_required
def mostrarAdministrarForos(request):
    foros = Foro.objects.all()
    datos = {'foros': foros}
    datos.update(get_session_data(request))
    return render(request, 'administrar_foros.html', datos)

@admin_required
def eliminarForo(request, id):
    foro = get_object_or_404(Foro, id=id)
    try:
        foro.delete()
        registrar_historial("Eliminación foro", request.session.get("idUsuario"))
    except Exception as e:
        errores = {'db_error': f'Error al eliminar el foro: {str(e)}'}
        foros = Foro.objects.all()
        datos = {'errores': errores, 'foros': foros}
        datos.update(get_session_data(request))
        return render(request, 'administrar_foros.html', datos)
    return redirect('administrar_foros')

@login_required
def mostrarCrearPublicacion(request, foro_id):
    foro = get_object_or_404(Foro, id=foro_id)
    datos = {'foro': foro}
    datos.update(get_session_data(request))
    return render(request, 'crear_publicacion.html', datos)

@login_required
def formCrearPublicacion(request, foro_id):
    titulo = request.POST.get('txtpubtit')
    comentario = request.POST.get('txtpubcom')

    usuario = obtener_usuario(request)
    foro = get_object_or_404(Foro, id=foro_id)

    try:
        Publicacion.objects.create(usuario=usuario, foro=foro, titulo=titulo, texto=comentario)
        
        registrar_historial("Creación publicación", usuario.id)

        return redirect('foro', foro_id=foro.id)
        
    except Exception as e:
        errores = {'db_error': f'Error al crear la publicación: {str(e)}'}
        datos = {'errores': errores, 'foro': foro}
        datos.update(get_session_data(request))
        return render(request, 'crear_publicacion.html', datos)

@login_required
def mostrarEditarPublicacion(request, foro_id, publicacion_id):
    foro = get_object_or_404(Foro, id=foro_id)
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    datos = {'foro': foro, 'publicacion': publicacion}
    datos.update(get_session_data(request))
    return render(request, 'editar_publicacion.html', datos)

@login_required
def formEditarPublicacion(request, foro_id, publicacion_id):
    foro = get_object_or_404(Foro, id=foro_id)
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    titulo = request.POST.get('txtpubtit')
    comentario = request.POST.get('txtpubcom')
    
    errores = {}

    publicacion.titulo = titulo
    publicacion.texto = comentario
    
    try:
        publicacion.save()
        
        registrar_historial("Edición de publicación", request.session.get("idUsuario"))

        return redirect('foro', foro_id=foro.id)
    except Exception as e:
        errores['db_error'] = f'Error al editar la publicación: {str(e)}'

    datos = {'errores': errores, 'foro': foro, 'publicacion': publicacion}
    datos.update(get_session_data(request))
    return render(request, 'editar_publicacion.html', datos)

@login_required
def mostrarPublicacion(request, foro_id, publicacion_id):
    foro = get_object_or_404(Foro, id=foro_id)
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    respuestas = Respuesta.objects.filter(publicacion=publicacion).order_by('fecha')
    datos = {'foro': foro, 'publicacion': publicacion, 'respuestas': respuestas}
    datos.update(get_session_data(request))
    return render(request, 'publicacion.html', datos)

@login_required
def eliminarPublicacion(request, foro_id, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id, foro_id=foro_id)
    try:
        publicacion.delete()
        registrar_historial("Eliminación publicación", request.session.get("idUsuario"))
    except Exception as e:
        errores = {'db_error': f'Error al eliminar la publicación: {str(e)}'}
        foro = get_object_or_404(Foro, id=foro_id)
        publicaciones = Publicacion.objects.filter(foro=foro)
        datos = {'errores': errores, 'foro': foro, 'publicaciones': publicaciones}
        datos.update(get_session_data(request))
        return render(request, 'ver_foro.html', datos)
    return redirect('foro', foro_id=foro_id)

@login_required
def formCrearRespuesta(request, foro_id, publicacion_id):
    texto_respuesta = request.POST.get('txtrespuesta')
    usuario = obtener_usuario(request)
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    foro = get_object_or_404(Foro, id=foro_id)

    if not texto_respuesta.strip():
        errores = {'texto': 'La respuesta no puede estar vacía.'}
        respuestas = Respuesta.objects.filter(publicacion=publicacion).order_by('fecha')
        datos = {'errores': errores, 'foro': foro, 'publicacion': publicacion, 'respuestas': respuestas}
        datos.update(get_session_data(request))
        return render(request, 'publicacion.html', datos)

    try:
        Respuesta.objects.create(usuario=usuario, publicacion=publicacion, texto=texto_respuesta)
        registrar_historial("Creación de respuesta", usuario.id)
        return redirect('mostrar_publicacion', foro_id=foro.id, publicacion_id=publicacion.id)
    except Exception as e:
        errores = {'db_error': f'Error al crear la respuesta: {str(e)}'}
        respuestas = Respuesta.objects.filter(publicacion=publicacion).order_by('fecha')
        datos = {'errores': errores, 'foro': foro, 'publicacion': publicacion, 'respuestas': respuestas}
        datos.update(get_session_data(request))
        return render(request, 'publicacion.html', datos)

@admin_required
def mostrarHistorialAcciones(request):
    historial = Historial.objects.all()
    datos = {'historial': historial}
    datos.update(get_session_data(request))
    return render(request, 'historial_acciones.html', datos)

def accesoDenegado(request):
    return render(request, 'acceso_denegado.html', {'mensaje': 'No tienes permiso para acceder a esta página.'})
