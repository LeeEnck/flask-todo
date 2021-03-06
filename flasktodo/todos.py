from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from . import db
import datetime

bp = Blueprint("todos", __name__)

@bp.route("/", methods=('GET', 'POST'))
def index():
    """View for home page which shows list of to-do items."""
    cur = db.get_db().cursor()

    if request.method == 'POST':
        task = request.form['task']
        error = None

        if not task:
            error = 'Task is required.'

        if error is None:
            #This inserts the user input into the database
            cur.execute(
                'INSERT INTO todos (description, completed,created_at) VALUES (%s,%s,%s)',
                (task, False, datetime.datetime.now())
            )
            g.db.commit()


    cur.execute('SELECT * FROM todos')
    todos = cur.fetchall()
    cur.close()

    return render_template("index.html", todos=todos)


@bp.route("/completed", methods=['GET', 'POST'])
def completed():


    cur = db.get_db().cursor()

    cur.execute('SELECT * FROM todos WHERE completed = True')
    todos = cur.fetchall()
    cur.close()

    return render_template("index.html", todos=todos)


@bp.route("/uncompleted", methods=['GET'])
def uncompleted():


    cur = db.get_db().cursor()

    cur.execute('SELECT * FROM todos WHERE completed = FALSE')
    todos = cur.fetchall()
    cur.close()

    return render_template("index.html", todos=todos)


@bp.route("/<int:id>/done", methods=('POST' ,))
def done(id):
    """This sets a task to completed"""
    cur = db.get_db().cursor()

    # Update the individual task and sets it to complete
    cur.execute(
        'UPDATE todos SET completed = True'
        ' WHERE id= %s ',
        (id,)
    )
    g.db.commit()

    cur.execute('SELECT * FROM todos')
    todos = cur.fetchall()
    cur.close()

    return redirect(url_for('todos.index'))


@bp.route("/<int:id>/delete", methods=('POST',))
def delete(id):
    """Sets the individual task to delete"""
    cur = db.get_db().cursor()

    #delete the actual task
    cur.execute(
    'DELETE FROM todos WHERE id= %s', (id,)
    )
    g.db.commit()
    cur.close()

    return redirect(url_for('todos.index'))
