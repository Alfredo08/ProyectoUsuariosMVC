from flask import render_template, request, redirect, session
from usuarios_app import app
from usuarios_app.modelos.modelo_departamentos import Departamento

@app.route( '/departamentos', methods=["GET"] )
def despliegaDepartamentos():
    listaDepartamentos = Departamento.obtenerListaDepartamentos()
    listaDepartamentosConUsuarios = Departamento.obtenerListaDepartamentosConUsuarios()
    print( listaDepartamentosConUsuarios )
    return render_template( "departamentos.html", listaDepartamentos=listaDepartamentos, listaDepartamentosConUsuarios=listaDepartamentosConUsuarios )