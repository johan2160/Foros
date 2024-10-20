from django.shortcuts import render, redirect
from .models import Usuario, Tematica, Foro, Post, Historial, Palabrotas


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

    comprobarLogin = Usuario.objects.filter(rut=rut, contraseña=pas).values()

    if comprobarLogin:
        nom_usu = comprobarLogin[0]['nombres']
        tip_usu = comprobarLogin[0]['tipo_usuario']

        # Guardar datos en sesión
        request.session["estadoSesion"] = True
        request.session["idUsuario"] = comprobarLogin[0]['id']
        request.session["nomUsuario"] = nom_usu  
        request.session["tipUsuario"] = tip_usu

        # Redirigir al index
        return redirect('index')
    
    else:
        datos = {'mensaje_error': 'Error de rut y/o contraseña'}
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
        mensaje_exito = {'mensaje_exito': 'Usuario registrado correctamente!'}
        return render(request, 'signup.html', mensaje_exito)
        
    except Exception as e:
        errores['db_error'] = f'Error al crear el usuario: {str(e)}'
        return render(request, 'signup.html', {'errores': errores})


# ---------- Logout ----------
def logout(request):
    request.session.flush()  # Elimina toda la sesión
    
    response = redirect('login')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
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

    usuario = Usuario.objects.get(id = id)

    errores = {}

    if pas_usu != pas2_usu:
        errores['contraseña'] = 'Las contraseñas no coinciden.'

    datos = {'errores': errores, 'usuario': usuario}

    if errores:
        return render(request, 'editar_perfil_usuario.html', datos)
    
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion:
        idUsuario = request.session.get("idUsuario")
        nomUsuario = request.session.get("nomUsuario")
        tipUsuario = request.session.get("tipUsuario")
    
    try:
        usuario.nombres = nom_usu
        usuario.materno = apem_usu
        usuario.paterno = apep_usu
        usuario.nacionalidad = nac_usu
        usuario.contraseña = pas_usu

        usuario.save()

        datos = {
            'usuario': usuario, 
            'mensaje_exito': 'Usuario actualizado correctamente!',
            'idUsuario': idUsuario,
            'nomUsuario': nomUsuario,
            'tipUsuario': tipUsuario,
            
            }

        return render(request, 'perfil_usuario.html', datos)
    except Exception as e:
        errores['db_error'] = f'Error al crear el usuario: {str(e)}'
        return render(request, 'editar_perfil_usuario.html', {'errores': errores})
    

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
        errores['nombre'] = f'La tematica: {nom_tematica} ya existe, intente crear otra.'

    if errores:
        return render(request, 'crear_tematica.html', {'errores': errores})
    
    try:
        tematica = Tematica(nombre=nom_tematica, descripcion=des_tematica)
        tematica.save()

        mensaje_exito = {'mensaje_exito': 'Tematica añadida correctamente!'}
        return render(request, 'crear_tematica.html', mensaje_exito)
    
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

        datos = {'tematica': tematica, 'mensaje_exito': 'Tematica actualizada correctamente!'}
        return render(request, 'editar_tematica.html', datos)
    
    except Exception as e:
        errores['db_error'] = f'Error al editar la tematica: {str(e)}'
        return render(request, 'editar_tematica.html', {'errores': errores})


def mostrarAdministrarTematicas(request):
    tematicas = Tematica.objects.all()
    datos = {'tematicas': tematicas}
    return render(request, 'administrar_tematicas.html', datos)


# ---------- Foro ----------
def mostrarForo(request):
    return render(request, 'ver_foro.html')

def mostrarCrearForo(request):
    tematicas = Tematica.objects.all()
    datos = {'tematicas': tematicas}
    return render(request, 'crear_foro.html', datos)

def formCrearForo(request):
    nom_foro = request.POST['txtnomfor']
    des_foro = request.POST['txtdesfor']
    tema = request.POST['cbotem']
    
    errores = {}
    tematicas = Tematica.objects.all()

    if verificarSiExiste(Foro, 'nombre', nom_foro):
        errores['nombre'] = f'El foro: {nom_foro} ya existe, intente con otro nombre.'

    if errores:
        return render(request, 'crear_foro.html', {'errores': errores, 'tematicas': tematicas})
    
    try:
        foro = Foro(nombre=nom_foro, descripcion=des_foro, tematica = tema)
        foro.save()
        
        datos = {'tematicas': tematicas, 'mensaje_exito': 'Tematica añadida correctamente!'}
        return render(request, 'crear_foro.html', datos)
    
    except Exception as e:
        errores['db_error'] = f'Error al crear el foro: {str(e)}'
        return render(request, 'crear_foro.html', {'errores': errores})

def mostrarEditarForo(request, id):
    foro = Foro.objects.get(id = id)
    tematicas = Tematica.objects.all()
    datos = {'foro': foro, 'tematicas': tematicas}
    return render(request, 'editar_foro.html', datos)

def formEditarForo(request, id):
    nom_foro = request.POST['txtnomfor']
    des_foro = request.POST['txtdesfor']
    tema_id = request.POST['cbotem']  # ID de la temática seleccionada

    errores = {}

    if verificarSiExiste(Foro, 'nombre', nom_foro):
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
        
        foro.save()
        
        foros = Foro.objects.all()
        datos = {'foros': foros, 'mensaje_exito': 'Foro actualizado correctamente!'}
        return render(request, 'administrar_foros.html', datos) 
    
    except Exception as e:
        errores['db_error'] = f'Error al editar el foro: {str(e)}'
        foro = Foro.objects.get(id=id)
        tematicas = Tematica.objects.all()
        datos = {'errores': errores, 'foro': foro, 'tematicas': tematicas}
        return render(request, 'editar_foro.html', datos)

    

def mostrarAdministrarForos(request):
    foros = Foro.objects.all()  
    datos = {'foros': foros}
    return render(request, 'administrar_foros.html', datos)


# ---------- Comentarios ----------
def mostrarCrearComentario(request):
    return render(request, 'crear_comentario.html')


def mostrarEditarComentario(request):
    return render(request, 'editar_comentario.html')


# ---------- Historial ----------
def mostrarHistorialAcciones(request):
    return render(request, 'historial_acciones.html')


# ---------- Utilidades ----------
def verificarSiExiste(clase, campo, valor):
    return clase.objects.filter(**{campo: valor}).exists()