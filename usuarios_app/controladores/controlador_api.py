from flask import request, session, jsonify, json
from usuarios_app import app
from usuarios_app.modelos.modelo_usuarios import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt( app )

@app.route( '/api/usuarios', methods=["GET"] )
def obtenerListaUsuarios():
    print( "Llego la petición" )
    listaUsuarios = Usuario.obtenerListaUsuariosAPI()
    return jsonify( listaUsuarios ), 200

@app.route( '/api/usuarios/crear', methods=["POST"] )
def agregarUsuario():
    nuevoUsuario = json.loads( request.data.decode( 'UTF-8' ) )
    passwordEncriptado = bcrypt.generate_password_hash( nuevoUsuario["password"] )
    nuevoUsuario["password"] = passwordEncriptado
    Usuario.agregaUsuario( nuevoUsuario )
    return jsonify({'mensaje': 'Usuario crearo exitosamente'}), 201

@app.route( '/api/usuarios/eliminar/<nombreusuario>', methods=["DELETE"] )
def eliminarUsuarioAPI( nombreusuario ):
    usuarioAEliminar = {
        "nombreusuario" : nombreusuario
    }

    existeUsuario = Usuario.obtenerDatosUsuario( usuarioAEliminar )
    if len(existeUsuario) == 0:
        return jsonify( {"mensaje": "Ese usuario no existe!" }), 404
    else:
        Usuario.eliminarUsuario( usuarioAEliminar )
        return jsonify( {} ), 204

# @app.route( '/api/usuarios/actualizar', methods=["PUT"] )
