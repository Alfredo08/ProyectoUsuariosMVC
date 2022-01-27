from usuarios_app import app
from usuarios_app.controladores import controlador_usuarios, controlador_departamentos

if __name__ == "__main__":
    app.run( debug = True )