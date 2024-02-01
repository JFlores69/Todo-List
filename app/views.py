import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from app.db import (get_db, get_task)

# Crea un Blueprint llamado 'tasks' con una URL base '/tasks'
bp = Blueprint('tasks', __name__, url_prefix='/tasks')

# Ruta para mostrar la lista de tareas
@bp.route('/')
def index():
    db = get_db()
    # Consulta la base de datos y recupera todas las tareas
    tasks = db.execute('SELECT * FROM task').fetchall()
    return render_template('tasks/index.html', tasks=tasks)

# Ruta para ver una tarea específica por su ID
@bp.route('/<int:id>')
def view(id):
    task = get_task(id)
    # Renderiza una plantilla HTML para mostrar los detalles de la tarea
    return render_template('tasks/view.html', task=task)

# Ruta para crear una nueva tarea
@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']
        error = None

        # Validación de campos requeridos
        if not titulo:
            error = 'El título es requerido.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            # Inserta la nueva tarea en la base de datos
            db.execute(
                'INSERT INTO task (titulo, contenido) VALUES (?, ?)',
                (titulo, contenido)
            )
            db.commit()
            # Redirige a la página principal de tareas después de la creación exitosa
            return redirect(url_for('tasks.index'))

    # Renderiza una plantilla HTML para mostrar el formulario de creación de tareas
    return render_template('tasks/create.html')

# Ruta para actualizar una tarea existente por su ID
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    task = get_task(id)

    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']
        error = None

        # Validación de campos requeridos
        if not titulo:
            error = 'El título es requerido.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            # Actualiza la tarea en la base de datos
            db.execute(
                'UPDATE task SET titulo = ?, contenido = ? WHERE id = ?',
                (titulo, contenido, id)
            )
            db.commit()
            # Redirige a la página principal de tareas después de la actualización exitosa
            return redirect(url_for('tasks.index'))

    # Renderiza una plantilla HTML para mostrar el formulario de actualización de tareas
    return render_template('tasks/update.html', task=task)

# Ruta para eliminar una tarea por su ID
@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    db = get_db()
    # Elimina la tarea de la base de datos
    db.execute('DELETE FROM task WHERE id = ?', (id,))
    db.commit()
    # Redirige a la página principal de tareas después de la eliminación exitosa
    return redirect(url_for('tasks.index'))
