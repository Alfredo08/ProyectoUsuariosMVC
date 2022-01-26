from flask import Flask, render_template, request, redirect, session
from usuarios_app import app
from usuarios_app.modelos.modelo_usuarios import Usuario

listaUsuarios = []

@app.route( '/', methods=['GET'] )
def despliegaRegistroLogin():
    return render_template( "index.html" )

@app.route( '/dashboard', methods=["GET"] )
def despliegaDashboard():
    if 'nombre' in session:
        return render_template( "dashboard.html", usuarios=listaUsuarios )
    else:
        return redirect( '/' )

@app.route( '/registroUsuario', methods=["POST"] )
def registrarUsuario():
    nuevoUsuario = {
        "nombre" : request.form["nombre"],
        "apellido" : request.form["apellido"],
        "nombreusuario" : request.form["usuario"],
        "password" : request.form["password"]
    }
    session["nombre"] = request.form["nombre"]
    session["apellido"] = request.form["apellido"]
    #listaUsuarios.append( nuevoUsuario )
    resultado = Usuario.agregaUsuario( nuevoUsuario )
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
        return redirect( '/' )
    else:
        session["nombre"] = resultado.nombre
        session["apellido"] = resultado.apellido
        return redirect( '/dashboard' )
    

@app.route( '/logout', methods=["GET"] )
def logoutUsuario():
    session.clear()
    return redirect( '/' )
