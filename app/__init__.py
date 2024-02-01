import os
from flask import Flask
from . import db  # Importa el módulo "db" desde el mismo paquete
from . import views  # Importa el módulo "views" desde el mismo paquete

def create_app(test_config=None):
    # Crea y configura la aplicación Flask
    app = Flask(__name__, instance_relative_config=True)

    # Configuración de la aplicación Flask
    app.config.from_mapping(
        SECRET_KEY='dev',  # Clave secreta para la aplicación (debería ser más segura en producción)
        DATABASE=os.path.join(app.instance_path, "Prueba.sqlite"),  # Ruta a la base de datos SQLite
        TEMPLATE_FOLDER='templates'  # Carpeta donde se encuentran las plantillas HTML
    )

    # Si hay una configuración de prueba proporcionada, cargarla.
    if test_config is None:
        # Carga la configuración desde un archivo "config.py" en la instancia si existe,
        # pero no durante las pruebas.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Carga la configuración de prueba si se proporciona.
        app.config.from_mapping(test_config)
    
    # Asegura que la carpeta de la instancia exista.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Inicializa la base de datos utilizando la función "init_app" del módulo "db".
    db.init_app(app)

    # Registra el Blueprint "views" en la aplicación.
    app.register_blueprint(views.bp)

    return app  # Retorna la instancia de la aplicación Flask creada
