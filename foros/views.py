from django.shortcuts import render, redirect
from .models import Usuario, Tematica, Foro, Post, Historial, Palabrotas


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


def mostrarLogin(request):
    if request.method == "POST":
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

    else:
        return render(request, 'login.html')

def verificarSiExiste(clase, campo, valor):
    return clase.objects.filter(**{campo: valor}).exists()

def mostrarSignup(request):
    
    if request.method == "POST":
        # Recogemos los datos del formulario
        rut_usu = request.POST['txtrut']
        nom_usu = request.POST['txtnom']
        apem_usu = request.POST['txtapem']
        apep_usu = request.POST['txtapep']
        ema_usu = request.POST['txtema']
        nac_usu = request.POST['txtnac']
        pas_usu = request.POST['txtpas']
        pas2_usu = request.POST['txtpas2']
        
        # Inicializamos un diccionario para los errores
        errores = {}

        # Verificar si las contraseñas coinciden primero
        if pas_usu != pas2_usu:
            errores['contraseña'] = 'Las contraseñas no coinciden.'
            
         # Verificar si el rut o el correo ya existen
        if verificarSiExiste(Usuario, 'rut', rut_usu):
            errores['rut'] = f'El rut: {rut_usu} ya existe.'
        
        if verificarSiExiste(Usuario, 'correo', ema_usu):
            errores['correo'] = f'El correo: {ema_usu} ya existe.'
            
        # Si hay errores, renderizamos la plantilla con los mensajes
        if errores:
            return render(request, 'signup.html', {'errores': errores})

        # Si no hay errores, procedemos a crear el usuario   
        try:
            usuario = Usuario(
                rut = rut_usu, 
                nombres = nom_usu, 
                paterno = apem_usu, 
                materno = apep_usu, 
                correo = ema_usu, 
                nacionalidad = nac_usu, 
                contraseña = pas_usu 
            )
            usuario.save()
            mensaje_exito = {'mensaje_exito': 'Usuario registrado correctamente!'}
            return render(request, 'signup.html', mensaje_exito)
            
        except Exception as e:
            errores['db_error'] = f'Error al crear el usuario: {str(e)}'
            return render(request, 'signup.html', {'errores': errores})
    
    return render(request, 'signup.html')


def logout(request):
    request.session.flush()  # Elimina toda la sesión
    
    response = redirect('login')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response


def mostrarPerfilUsuario(request, id):
    usuario = Usuario.objects.get(id = id)
    
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


def mostrarCrearTematica(request):
    if request.method == "POST":
        nom_tematica = request.POST['txtnomtem']
        des_tematica = request.POST['txtdestem']
        
        errores = {}
            
        # Verificar si la tematica ya existe
        if verificarSiExiste(Tematica, 'nombre', nom_tematica):
            errores['nombre'] = f'La tematica: {nom_tematica} ya existe, intente crear otra.'
            
        # Si hay errores, renderizamos la plantilla con los mensajes
        if errores:
            return render(request, 'crear_tematica.html', {'errores': errores})
        
        try:
            tematica = Tematica(nombre = nom_tematica, descripcion = des_tematica)
            tematica.save()

            mensaje_exito = {'mensaje_exito': 'Tematica añadida correctamente!'}
            return render(request, 'crear_tematica.html', mensaje_exito)
        
        except Exception as e:
            errores['db_error'] = f'Error al crear la tematica: {str(e)}'
            return render(request, 'crear_tematica.html', {'errores': errores})
        
    return render(request, 'crear_tematica.html')

def mostrarEditarTematica(request, id):
    if request.method == "GET":
        tematica = Tematica.objects.get(id = id)
        datos = {'tematica': tematica}
        return render(request, 'editar_tematica.html', datos)
    
    if request.method == "POST":
        nom_tematica = request.POST['txtnomtem']
        des_tematica = request.POST['txtdestem']
        
        errores = {}
            
        # Verificar si la tematica ya existe
        if verificarSiExiste(Tematica, 'nombre', nom_tematica):
            errores['nombre'] = f'La tematica: {nom_tematica} ya existe.'
            
        # Si hay errores, renderizamos la plantilla con los mensajes
        if errores:
            tematica = Tematica.objects.get(id=id)
            return render(request, 'editar_tematica.html', {'errores': errores, 'tematica': tematica})
        
        try:
            tematica = Tematica.objects.get(id = id)
            
            tematica.nombre = nom_tematica
            tematica.descripcion = des_tematica
            tematica.save()

            datos = {'tematica': tematica, 'mensaje_exito': 'Tematica actualizada correctamente!'}
            return render(request, 'editar_tematica.html', datos)
        
        except Exception as e:
            errores['db_error'] = f'Error al editar la tematica: {str(e)}'
            return render(request, f'editar_tematica.html', {'errores': errores})


def mostrarAdministrarTematicas(request):
    tematicas = Tematica.objects.all().values()
    datos = {'tematicas': tematicas}
    
    return render(request, 'administrar_tematicas.html', datos)


def mostrarGestionarUsuarios(request):
    return render(request, 'gestionar_usuarios.html')


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


def mostrarHistorialAcciones(request):
    return render(request, 'historial_acciones.html')