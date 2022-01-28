from flask import render_template, request, redirect, session, flash
from usuarios_app import app
from usuarios_app.modelos.modelo_usuarios import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt( app )

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
    passwordEncriptado = bcrypt.generate_password_hash( request.form["password"] )
    nuevoUsuario = {
        "nombre" : request.form["nombre"],
        "apellido" : request.form["apellido"],
        "nombreusuario" : request.form["usuario"],
        "password" : passwordEncriptado,
        "id_departamento" : request.form["departamento"]
    }
    session["nombre"] = request.form["nombre"]
    session["apellido"] = request.form["apellido"]
    resultado = Usuario.agregaUsuario( nuevoUsuario )

    # ToDo: Validar resultado que nos arroja 0
    if type( resultado ) is int and resultado == 0:
        return redirect( '/dashboard' )
    else:
        flash( "Hubo un problema con el registro, intenta con otro nombre de usuario", "registro" )
        return redirect( '/' )

@app.route( '/login', methods=["POST"] )
def loginUsuario():
    loginUsuario = request.form["loginUsuario"]
    passwordUsuario = request.form["passwordUsuario"]

    usuario = {
        "nombreusuario" : loginUsuario
    }

    resultado = Usuario.verificaUsuario( usuario )

    if resultado == None:
        flash( "El nombre de usuario esta escrito incorrectamente", "login" )
        return redirect( '/' )
    else:
        print( resultado.password[0] )
        print( passwordUsuario )
        if not bcrypt.check_password_hash( resultado.password[0], passwordUsuario ):
            flash( "El password es incorrecto", "login" )
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

