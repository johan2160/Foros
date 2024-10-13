from django.shortcuts import render, redirect
from .models import Usuario, Tematica, Foro, Post, Historial, Palabrotas


def mostrarIndex(request):
    estadoSesion = request.session.get("estadoSesion")

    if estadoSesion:
        nomUsuario = request.session.get("nomUsuario")
        tipUsuario = request.session.get("tipUsuario")

        # Pasar los datos al template
        return render(request, 'index.html', {'nomUsuario': nomUsuario, 'tipUsuario': tipUsuario})
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

def verificarSiExiste(clase, campoAVerificar, valor):
    filtro = {f"{campoAVerificar}": valor}
    
    existe = clase.objects.filter(**filtro).exists()
    
    if existe:
        return {'mensaje_error': f'El {campoAVerificar} con valor "{valor}" ya existe!'}
    else:
        return None   

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
            print(errores)
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
    try:
        del request.session["estadoSesion"]
        del request.session["idUsuario"]
        del request.session["nomUsuario"]
        del request.session["tipUsuario"]

    # Capturar errores relacionados con las claves de la sesión que no existan
    except KeyError:
        pass

    return redirect('login')


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