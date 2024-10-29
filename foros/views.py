from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from .models import Usuario, Tematica, Foro, Publicacion, Historial, Palabrotas


# ---------- Index ----------
def mostrarIndex(request):
    estadoSesion = request.session.get("estadoSesion")

    if estadoSesion:
        idUsuario = request.session.get("idUsuario")
        nomUsuario = request.session.get("nomUsuario")
        tipUsuario = request.session.get("tipUsuario")
        
        datos = {
            'idUsuario': idUsuario,
            'nomUsuario': nomUsuario,
            'tipUsuario': tipUsuario,
        }

        return render(request, 'index.html', datos)
    else:
        return redirect('login')


# ---------- Login ----------
def mostrarLogin(request):
    return render(request, 'login.html')


def formLogin(request):
    rut = request.POST["txtrut"]
    pas = request.POST["txtpas"]

    try:
        usuario = Usuario.objects.get(rut=rut)
    except Usuario.DoesNotExist:
        datos = {'mensaje_error': 'Usuario no encontrado.'}
        return render(request, 'login.html', datos)

    if usuario.estado == 'Suspendido':
        datos = {'mensaje_error': 'Su cuenta está suspendida. Contacte al administrador.'}
        return render(request, 'login.html', datos)

    if usuario.contraseña == pas:
        # Restablecer intentos fallidos
        usuario.intentos_fallidos = 0
        usuario.save()

        # Iniciar sesión
        request.session["estadoSesion"] = True
        request.session["idUsuario"] = usuario.id
        request.session["nomUsuario"] = usuario.nombres  
        request.session["tipUsuario"] = usuario.tipo_usuario
        
        # Registrar en historial
        accion = "Inicia sesión"
        fecha = datetime.now()
        his = Historial(accion=accion, fecha=fecha, usuario_id=usuario.id)
        his.save()

        return redirect('index')
    else:
        usuario.intentos_fallidos += 1
        usuario.save()

        if usuario.intentos_fallidos >= 3:
            usuario.estado = 'Suspendido'
            usuario.save()
            datos = {'mensaje_error': 'Su cuenta ha sido suspendida por múltiples intentos fallidos.'}
        else:
            intentos_restantes = 3 - usuario.intentos_fallidos
            datos = {'mensaje_error': f'Contraseña incorrecta. Intentos restantes: {intentos_restantes}'}
        
        return render(request, 'login.html', datos)



# ---------- Signup ----------
def mostrarSignup(request):
    return render(request, 'signup.html')


def formSignup(request):
    rut_usu = request.POST['txtrut']
    nom_usu = request.POST['txtnom']
    apem_usu = request.POST['txtapem']
    apep_usu = request.POST['txtapep']
    ema_usu = request.POST['txtema']
    nac_usu = request.POST['txtnac']
    pas_usu = request.POST['txtpas']
    pas2_usu = request.POST['txtpas2']
    
    errores = {}

    if pas_usu != pas2_usu:
        errores['contraseña'] = 'Las contraseñas no coinciden.'
        
    if verificarSiExiste(Usuario, 'rut', rut_usu):
        errores['rut'] = f'El rut: {rut_usu} ya existe.'
    
    if verificarSiExiste(Usuario, 'correo', ema_usu):
        errores['correo'] = f'El correo: {ema_usu} ya existe.'
        
    if errores:
        return render(request, 'signup.html', {'errores': errores})

    try:
        usuario = Usuario(
            rut=rut_usu,
            nombres=nom_usu,
            paterno=apem_usu,
            materno=apep_usu,
            correo=ema_usu,
            nacionalidad=nac_usu,
            contraseña=pas_usu
        )
        usuario.save()
        
        accion = "Registro de usuario"
        fecha = datetime.now()
        usuario_hist = usuario.id  
        his = Historial(accion=accion, fecha=fecha, usuario_id=usuario_hist)
        his.save()  

        request.session['mensaje_exito'] = 'Usuario registrado correctamente!'
        return redirect('login')  # Redirige a login tras registro exitoso
        
    except Exception as e:
        errores['db_error'] = f'Error al crear el usuario: {str(e)}'
        return render(request, 'signup.html', {'errores': errores})


# ---------- Logout ----------
def logout(request):
    accion = "Cierre sesión"
    fecha = datetime.now()
    usuario = request.session["idUsuario"]
    his = Historial(accion = accion, fecha = fecha, usuario_id = usuario)
    his.save()
    
    request.session.flush()  # Elimina toda la sesión
    
    response = redirect('login')    
    return response


# ---------- Perfil Usuario ----------
def mostrarPerfilUsuario(request, id):
    usuario = Usuario.objects.get(id=id)
    
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion:
        idUsuario = request.session.get("idUsuario")
        nomUsuario = request.session.get("nomUsuario")
        tipUsuario = request.session.get("tipUsuario")
        
        datos = {
            'usuario': usuario,
            'idUsuario': idUsuario,
            'nomUsuario': nomUsuario,
            'tipUsuario': tipUsuario,
        }
        return render(request, 'perfil_usuario.html', datos)
    else:
        return redirect('login')


def mostrarEditarPerfilUsuario(request, id):
    usuario = Usuario.objects.get(id = id)
    datos = {'usuario': usuario}
    return render(request, 'editar_perfil_usuario.html', datos)


def formEditarPerfilUsuario(request, id):
    nom_usu = request.POST['txtnom']
    apem_usu = request.POST['txtapem']
    apep_usu = request.POST['txtapep']
    nac_usu = request.POST['txtnac']
    pas_usu = request.POST['txtpas']
    pas2_usu = request.POST['txtpas2']

    usuario = Usuario.objects.get(id=id)

    errores = {}

    if pas_usu != pas2_usu:
        errores['contraseña'] = 'Las contraseñas no coinciden.'

    if errores:
        datos = {'errores': errores, 'usuario': usuario}
        return render(request, 'editar_perfil_usuario.html', datos)

    try:
        usuario.nombres = nom_usu
        usuario.materno = apem_usu
        usuario.paterno = apep_usu
        usuario.nacionalidad = nac_usu
        usuario.contraseña = pas_usu
        usuario.save()
        
        accion = "Edición perfil"
        fecha = datetime.now()
        usuario_hist = request.session["idUsuario"]
        his = Historial(accion=accion, fecha=fecha, usuario_id=usuario_hist)
        his.save() 

        return redirect('perfil_usuario', id=usuario.id)
    except Exception as e:
        errores['db_error'] = f'Error al actualizar el usuario: {str(e)}'
        datos = {'errores': errores, 'usuario': usuario}
        return render(request, 'editar_perfil_usuario.html', datos)
    

def mostrarGestionarUsuarios(request):
    usuarios = Usuario.objects.all()
    datos = {'usuarios': usuarios}
    return render(request, 'gestionar_usuarios.html', datos)


# ---------- Temáticas ----------
def mostrarCrearTematica(request):
    return render(request, 'crear_tematica.html')


def formCrearTematica(request):
    nom_tematica = request.POST['txtnomtem']
    des_tematica = request.POST['txtdestem']
    
    errores = {}

    if verificarSiExiste(Tematica, 'nombre', nom_tematica):
        errores['nombre'] = f'La tematica: {nom_tematica} ya existe.'

    if errores:
        return render(request, 'crear_tematica.html', {'errores': errores})
    
    try:
        tematica = Tematica(nombre=nom_tematica, descripcion=des_tematica)
        tematica.save()
        
        accion = "Creación de temática"
        fecha = datetime.now()
        usuario_hist = request.session["idUsuario"]
        his = Historial(accion=accion, fecha=fecha, usuario_id=usuario_hist)
        his.save() 

        return redirect('administrar_tematicas')
    
    except Exception as e:
        errores['db_error'] = f'Error al crear la tematica: {str(e)}'
        return render(request, 'crear_tematica.html', {'errores': errores})

def mostrarEditarTematica(request, id):
    tematica = Tematica.objects.get(id=id)
    datos = {'tematica': tematica}
    return render(request, 'editar_tematica.html', datos)


def formEditarTematica(request, id):
    nom_tematica = request.POST['txtnomtem']
    des_tematica = request.POST['txtdestem']
    
    errores = {}

    if verificarSiExiste(Tematica, 'nombre', nom_tematica):
        errores['nombre'] = f'La tematica: {nom_tematica} ya existe.'
        
    if errores:
        tematica = Tematica.objects.get(id=id)
        return render(request, 'editar_tematica.html', {'errores': errores, 'tematica': tematica})
    
    try:
        tematica = Tematica.objects.get(id=id)
        tematica.nombre = nom_tematica
        tematica.descripcion = des_tematica
        tematica.save()
        
        accion = "Edición de temática"
        fecha = datetime.now()
        usuario_hist = request.session["idUsuario"]
        his = Historial(accion=accion, fecha=fecha, usuario_id=usuario_hist)
        his.save() 

        return redirect('administrar_tematicas')  # Redirige a la administración de temáticas tras editar exitosamente
    
    except Exception as e:
        errores['db_error'] = f'Error al editar la tematica: {str(e)}'
        tematica = Tematica.objects.get(id=id)
        return render(request, 'editar_tematica.html', {'errores': errores, 'tematica': tematica})

def eliminarTematica(request, id):
    try:
        tematica = Tematica.objects.get(id=id)
        
        accion = "Eliminación tematica"
        fecha = datetime.now()
        usuario = request.session["idUsuario"]
        his = Historial(accion=accion, fecha=fecha, usuario_id=usuario)
        his.save()

        tematica.delete()

        tematicas = Tematica.objects.all()

        datos = {
            'mensaje_exito': 'Tematica eliminada correctamente!',
            'tematicas': tematicas
        }
    except:
        datos = {
            'mensaje_error': 'La temática que intentas eliminar no existe.',
            'tematicas': Tematica.objects.all() 
        }
    return render(request, 'administrar_tematicas.html', datos)


def mostrarAdministrarTematicas(request):
    tematicas = Tematica.objects.all()
    datos = {'tematicas': tematicas}
    return render(request, 'administrar_tematicas.html', datos)


# ---------- Foro ----------
def mostrarForo(request, foro_id):
    foro = Foro.objects.get(id = foro_id)
    publicaciones = Publicacion.objects.filter(foro = foro)
    datos = {'foro': foro, 'publicaciones': publicaciones}
    return render(request, 'ver_foro.html', datos)

def mostrarCrearForo(request):
    tematicas = Tematica.objects.all()
    datos = {'tematicas': tematicas}
    return render(request, 'crear_foro.html', datos)

def formCrearForo(request):
    if request.method == 'POST':
        nom_foro = request.POST['txtnomfor']
        des_foro = request.POST['txtdesfor']
        tema_id = request.POST['cbotem']
        imagen = request.FILES.get('imagen')  # Obtener el archivo de imagen si se sube uno

        tematicas = Tematica.objects.all()
        errores = {}

        if verificarSiExiste(Foro, 'nombre', nom_foro):
            errores['nombre'] = f'El foro: {nom_foro} ya existe, intente con otro nombre.'

        if errores:
            datos = {'errores': errores, 'tematicas': tematicas}
            return render(request, 'crear_foro.html', datos)

        try:
            tematica = Tematica.objects.get(id=tema_id)
            foro = Foro(nombre=nom_foro, descripcion=des_foro, tematica=tematica)

            if imagen:
                foro.imagen = imagen  # Guardar la imagen si se sube una

            foro.save()

            accion = "Creación de foro"
            fecha = datetime.now()
            usuario_hist = request.session["idUsuario"]  # ID del usuario que crea el foro
            his = Historial(accion=accion, fecha=fecha, usuario_id=usuario_hist)
            his.save()

            return redirect('administrar_foros')  # Redirigir a la administración de foros tras la creación exitosa

        except Exception as e:
            errores['db_error'] = f'Error al crear el foro: {str(e)}'
            datos = {'errores': errores, 'tematicas': tematicas}
            return render(request, 'crear_foro.html', datos)
    else:
        tematicas = Tematica.objects.all()
        datos = {'tematicas': tematicas}
        return render(request, 'crear_foro.html', datos)


def mostrarEditarForo(request, id):
    foro = Foro.objects.get(id = id)
    tematicas = Tematica.objects.all()
    datos = {'foro': foro, 'tematicas': tematicas}
    return render(request, 'editar_foro.html', datos)

def formEditarForo(request, id):
    if request.method == 'POST':
        nom_foro = request.POST['txtnomfor']
        des_foro = request.POST['txtdesfor']
        tema_id = request.POST['cbotem']
        imagen = request.FILES.get('imagen')  # Obtener el archivo de imagen si se subió uno

        errores = {}

        # Verificar si el nombre del foro ya existe en otro foro (excluyendo el actual)
        if Foro.objects.filter(nombre=nom_foro).exclude(id=id).exists():
            errores['nombre'] = f'El foro: {nom_foro} ya existe, intente con otro nombre.'
        
        if errores:
            foro = Foro.objects.get(id=id)
            tematicas = Tematica.objects.all()
            datos = {'foro': foro, 'tematicas': tematicas, 'errores': errores}
            return render(request, 'editar_foro.html', datos)
        
        try:
            foro = Foro.objects.get(id=id)
            foro.nombre = nom_foro
            foro.descripcion = des_foro

            # Obtener la instancia de la temática seleccionada
            tematica = Tematica.objects.get(id=tema_id)
            foro.tematica = tematica

            if imagen:
                foro.imagen = imagen  # Actualizar la imagen si se subió una nueva

            foro.save()
            
            accion = "Edición foro"
            fecha = datetime.now()
            usuario = request.session["idUsuario"]
            his = Historial(accion=accion, fecha=fecha, usuario_id=usuario)
            his.save()
            
            # Redirigir al usuario a la página de administración de foros con un mensaje de éxito
            messages.success(request, 'Foro actualizado correctamente!')
            return redirect('administrar_foros')
        
        except Exception as e:
            errores['db_error'] = f'Error al editar el foro: {str(e)}'
            foro = Foro.objects.get(id=id)
            tematicas = Tematica.objects.all()
            datos = {'errores': errores, 'foro': foro, 'tematicas': tematicas}
            return render(request, 'editar_foro.html', datos)
    else:
        return redirect('editar_foro', id=id)



def mostrarAdministrarForos(request):
    foros = Foro.objects.all()  
    datos = {'foros': foros}
    return render(request, 'administrar_foros.html', datos)

def eliminarForo(request, id):
    try:
        foro = Foro.objects.get(id=id)
        
        # Guardar la acción en el historial
        accion = "Eliminación foro"
        fecha = datetime.now()
        usuario = request.session["idUsuario"]
        his = Historial(accion=accion, fecha=fecha, usuario_id=usuario)
        his.save()

        # Eliminar el foro
        foro.delete()

        # Obtener la lista de foros actualizada
        foros = Foro.objects.all()

        # Preparar los datos para la plantilla
        datos = {
            'mensaje_exito': 'Foro eliminado correctamente!',
            'foros': foros 
        }

    except:
        # En caso de que el foro no exista, mostramos un mensaje o redirigimos
        datos = {
            'mensaje_error': 'El foro que intentas eliminar no existe.',
            'foros': Foro.objects.all()
        }
    return render(request, 'administrar_foros.html', datos)


# ---------- Comentarios ----------
def mostrarCrearPublicacion(request, foro_id):
    foro = Foro.objects.get(id = foro_id)
    datos = {'foro': foro}
    return render(request, 'crear_publicacion.html', datos)

def formCrearPublicacion(request, foro_id):
    titulo = request.POST['txtpubtit']
    comentario = request.POST['txtpubcom']
    
    idUsuario = request.session.get("idUsuario")
    usuario = Usuario.objects.get(id=idUsuario)
    
    foro = Foro.objects.get(id=foro_id)
    
    try:
        publicacion = Publicacion(usuario=usuario, foro=foro, titulo=titulo, texto=comentario)
        publicacion.save()
        
        accion = "Creación publicación"
        fecha = datetime.now()
        usuario = request.session["idUsuario"]
        his = Historial(accion=accion, fecha=fecha, usuario_id=usuario)
        his.save()

        return redirect('foro', foro_id=foro.id)
        
    except Exception as e:
        errores = {'db_error': f'Error al crear la publicacion: {str(e)}'}
        return render(request, 'crear_publicacion.html', {'errores': errores, 'foro': foro})



def mostrarEditarPublicacion(request, foro_id, publicacion_id):
    foro = Foro.objects.get(id = foro_id)
    publicacion = Publicacion.objects.get(id = publicacion_id)
    datos = {'foro': foro, 'publicacion': publicacion}
    return render(request, 'editar_publicacion.html', datos)

def formEditarPublicacion(request, foro_id, publicacion_id):
    foro = Foro.objects.get(id=foro_id)
    publicacion = Publicacion.objects.get(id=publicacion_id)
    errores = {}

    if request.method == 'POST':
        titulo = request.POST.get('txtpubtit')
        comentario = request.POST.get('txtpubcom')
        publicacion.titulo = titulo
        publicacion.texto = comentario
        
        try:
            publicacion.save()
            
            accion = "Edición de publicación"
            fecha = datetime.now()
            usuario = request.session["idUsuario"]  # Suponiendo que el idUsuario está en la sesión
            his = Historial(accion=accion, fecha=fecha, usuario_id=usuario)
            his.save()
            
            messages.success(request, 'La publicación ha sido actualizada exitosamente.')
            # quiero mostrar un mensaje de exito (Como lo puedo lograr?)
            return redirect('foro', foro_id=foro.id)
        except Exception as e:
            errores['db_error'] = f'Error al editar la publicación: {str(e)}'

    datos = {
        'errores': errores,
        'foro': foro,
        'publicacion': publicacion,
    }
    return render(request, 'editar_publicacion.html', datos)  


# ---------- Historial ----------
def mostrarHistorialAcciones(request):
    historial = Historial.objects.all()
    datos = { 'historial': historial }
    return render(request, 'historial_acciones.html', datos)


# ---------- Utilidades ----------
def verificarSiExiste(clase, campo, valor):
    return clase.objects.filter(**{campo: valor}).exists()