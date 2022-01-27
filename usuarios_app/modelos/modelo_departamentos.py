from usuarios_app.config.mysqlconnection import connectToMySQL
from usuarios_app.modelos.modelo_usuarios import Usuario

class Departamento:
    def __init__( self, id, nombre ):
        self.id = id
        self.nombre = nombre
        self.usuarios = []
    
    def agregaUsuario( self, usuario ):
        self.usuarios.append( usuario )

    @classmethod
    def obtenerListaDepartamentos( cls ):
        query = "SELECT * FROM departamentos;"
        resultado = connectToMySQL( 'usuarios_db' ).query_db( query )
        listaDepartamentos = []
        for departamento in resultado:
            listaDepartamentos.append( cls( departamento["id"], departamento["nombre"]) )
        return listaDepartamentos

    @classmethod
    def obtenerListaDepartamentosConUsuarios( cls ):
        query = "SELECT * FROM departamentos d LEFT JOIN usuarios u ON d.id = u.id_departamento;"
        resultado = connectToMySQL( "usuarios_db" ).query_db( query )
        listaDepartamentosConUsuarios = []

        for renglon in resultado:
            indice = existeDepartamentoEnArreglo( renglon["id"], listaDepartamentosConUsuarios )
            if indice == -1:
                departamentoAAgregar = Departamento(renglon['id'], renglon['nombre'])
                departamentoAAgregar.agregaUsuario( Usuario(renglon["u.nombre"], renglon["apellido"], renglon["nombreusuario"], renglon["password"], renglon["id"]) )
                listaDepartamentosConUsuarios.append( departamentoAAgregar )
            else:
                listaDepartamentosConUsuarios[indice].agregaUsuario( Usuario(renglon["u.nombre"], renglon["apellido"], renglon["nombreusuario"], renglon["password"], renglon["id"]) )
        
        return listaDepartamentosConUsuarios

def existeDepartamentoEnArreglo( id_dep, listaDepartamentos ):
    for i in range( 0, len(listaDepartamentos)):
        if listaDepartamentos[i].id == id_dep:
            return i
    return -1
