from usuarios_app import app
from usuarios_app.controladores import controlador_usuarios, controlador_departamentos, controlador_api

if __name__ == "__main__":
    app.run( debug = True )