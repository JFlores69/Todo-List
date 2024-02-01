import sqlite3
from flask import current_app, g
from flask.cli import with_appcontext
import click

# Función para obtener la conexión a la base de datos
def get_db():
    if 'db' not in g:
        # Si no hay una conexión en el contexto global (g), se crea una nueva conexión a la base de datos SQLite
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row  # Configura el modo de recuperación de filas como diccionarios

    return g.db

# Función para cerrar la conexión a la base de datos
def close_db(e=None):
    db = g.pop('db', None)  # Obtiene la conexión desde el contexto global y la elimina si existe

    if db is not None:
        db.close()

# Función para inicializar la base de datos utilizando un archivo SQL de esquema
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        # Ejecuta el contenido del archivo 'schema.sql' en la base de datos para crear tablas y esquema
        db.executescript(f.read().decode('utf8'))

# Función para obtener una tarea específica por su ID
def get_task(id):
    db = get_db()
    task = db.execute('SELECT * FROM task WHERE id = ?', (id,)).fetchone()
    return task

# Comando de Flask para inicializar la base de datos desde la línea de comandos
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Inicializar la base de datos."""
    init_db()
    click.echo('Base de datos inicializada.')

# Función para inicializar la aplicación Flask con las funciones de base de datos
def init_app(app):
    app.teardown_appcontext(close_db)  # Registra la función para cerrar la base de datos al finalizar la solicitud
    app.cli.add_command(init_db_command)  # Agrega el comando 'init-db' para inicializar la base de datos desde la CLI de Flask
