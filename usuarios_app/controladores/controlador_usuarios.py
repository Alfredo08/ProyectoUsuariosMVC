from flask import render_template, request, redirect, session
from usuarios_app import app
from usuarios_app.modelos.modelo_usuarios import Usuario

@app.route( '/', methods=['GET'] )
def despliegaRegistroLogin():
    return render_template( "index.html" )

@app.route( '/dashboard', methods=["GET"] )
def despliegaDashboard():
    if 'nombre' in session:
        listaUsuarios = Usuario.obtenerListaUsuarios()
        return render_template( "dashboard.html", usuarios=listaUsuarios )
    else:
        return redirect( '/' )

@app.route( '/registroUsuario', methods=["POST"] )
def registrarUsuario():
    nuevoUsuario = {
        "nombre" : request.form["nombre"],
        "apellido" : request.form["apellido"],
        "nombreusuario" : request.form["usuario"],
        "password" : request.form["password"],
        "id_departamento" : request.form["departamento"]
    }
    session["nombre"] = request.form["nombre"]
    session["apellido"] = request.form["apellido"]
    resultado = Usuario.agregaUsuario( nuevoUsuario )

    # ToDo: Validar resultado que nos arroja 0
    if resultado == False:
        return redirect( '/' )
    else:
        return redirect( '/dashboard' )

@app.route( '/login', methods=["POST"] )
def loginUsuario():
    loginUsuario = request.form["loginUsuario"]
    passwordUsuario = request.form["passwordUsuario"]

    usuario = {
        "nombreusuario" : loginUsuario,
        "password" : passwordUsuario
    }

    resultado = Usuario.verificaUsuario( usuario )

    if resultado == None:
        # ToDO: Agregar mensajes de validaciones 
        return redirect( '/' )
    else:
        session["nombre"] = resultado.nombre
        session["apellido"] = resultado.apellido
        return redirect( '/dashboard' )


@app.route( '/logout', methods=["GET"] )
def logoutUsuario():
    session.clear()
    return redirect( '/' )

@app.route( '/usuario/remover/<idUsuario>', methods=["POST"] )
def eliminarUsuario( idUsuario ):
    usuarioAEliminar = {
        "nombreusuario": idUsuario
    }
    resultado = Usuario.eliminarUsuario( usuarioAEliminar )
    print( resultado )
    return redirect( '/dashboard' )

@app.route( '/usuario/editar/<idUsuario>', methods=["GET"] )
def despliegaEditar( idUsuario ):
    usuarioAEditar = {
        "nombreusuario" : idUsuario
    }
    resultado = Usuario.obtenerDatosUsuario( usuarioAEditar )
    return render_template( "editarUsuario.html", usuario=resultado[0] )

@app.route( '/usuario/editar/<idUsuario>', methods=["POST"] )
def editarUsuario( idUsuario ):
    usuarioAEditar = {
        "nombreusuario" : idUsuario,
        "nombre" : request.form["nombre"],
        "apellido" : request.form["apellido"],
        "password" : request.form["password"],
        "id_departamento" : request.form["departamento"]
    }
    resultado = Usuario.editarUsuario( usuarioAEditar )

    # ToDo: Validar que el usuario editado sea el de la sesión
    session["nombre"] = request.form["nombre"]
    session["apellido"] = request.form["apellido"]
    return redirect( '/dashboard' )

