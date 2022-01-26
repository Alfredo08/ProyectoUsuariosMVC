from usuarios_app.config.mysqlconnection import connectToMySQL

class Usuario:
    def __init__( self, nombre, apellido, nombreusuario, password ):
        self.nombre = nombre
        self.apellido = apellido
        self.nombreusuario = nombreusuario
        self.password = password
    
    @classmethod
    def agregaUsuario( cls, nuevoUsuario ):
        query = "INSERT INTO usuarios(nombre, apellido, nombreusuario, password) VALUES(%(nombre)s, %(apellido)s, %(nombreusuario)s, %(password)s);"
        resultado = connectToMySQL( "usuarios_db" ).query_db( query, nuevoUsuario )
        return resultado
    
    @classmethod
    def verificaUsuario( cls, usuario ):
        query = "SELECT * FROM usuarios WHERE nombreusuario = %(nombreusuario)s AND password = %(password)s;"
        resultado = connectToMySQL( "usuarios_db" ).query_db( query, usuario )
        if len( resultado ) > 0:
            usuarioResultado = Usuario( resultado[0]["nombre"], resultado[0]["apellido"], resultado[0]["nombreusuario"], resultado[0]["password"] )
            return usuarioResultado
        else:
            return None

    @classmethod
    def obtenerListaUsuarios( self ):
        query = "SELECT * FROM usuarios;"
        resultado = connectToMySQL( "usuarios_db" ).query_db( query )
        listaUsuarios = []
        for usuario in resultado:
            listaUsuarios.append( Usuario( usuario["nombre"], usuario["apellido"], usuario["nombreusuario"], usuario["password"]) )
        return listaUsuarios
    
    @classmethod
    def eliminarUsuario( self, usuario ):
        query = "DELETE FROM usuarios WHERE nombreusuario = %(nombreusuario)s;"
        resultado = connectToMySQL( "usuarios_db" ).query_db( query, usuario )
        return resultado

    @classmethod
    def obtenerDatosUsuario( self, usuario ):
        query = "SELECT * FROM usuarios WHERE nombreusuario = %(nombreusuario)s;"
        resultado = connectToMySQL( "usuarios_db" ).query_db( query, usuario )
        return resultado
    
    @classmethod
    def editarUsuario( self, usuarioAEditar ):
        query = "UPDATE usuarios SET nombre = %(nombre)s, apellido = %(apellido)s, password = %(password)s WHERE nombreusuario = %(nombreusuario)s;"
        resultado = connectToMySQL( "usuarios_db" ).query_db( query, usuarioAEditar )
        return resultado
