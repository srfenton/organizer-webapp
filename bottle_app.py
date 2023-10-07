from bottle import default_app, route, get, post, request, redirect, template
from setup import setup_table
import sqlite3


connection = sqlite3.connect("daily_list.db")

@route('/')
def get_index():
    return template("index.tpl")

@route('/legacy')
def get_daily_list():
    return template("daily_list.tpl")

@route('/list')
def get_list():
    cursor = connection.cursor()
    rows = cursor.execute("select id, task, complete from list")
    rows = list(rows)
    rows = [ {'id':row[0] ,'task':row[1], 'complete':row[2]} for row in rows ]
    uncompleted_list = []
    for x in range(0,len(rows)):
        if rows[x]['complete']== False:
            uncompleted_list.append(rows[x])
    return template("daily_list.tpl", name="sf", task_list=uncompleted_list)


@route("/complete/<id>")
def get_complete_task(id):
    cursor = connection.cursor()
    cursor.execute(f"update list set complete = true where id={id}")
    connection.commit()
    redirect('/list')


@route("/undo-complete/<id>")
def get_undo_complete_task(id):
    cursor = connection.cursor()
    cursor.execute(f"update list set complete = false where id={id}")
    connection.commit()
    redirect('/completed-list')

@route("/completed-list")
def get_complete():
    cursor = connection.cursor()
    rows = cursor.execute("select id, task, complete from list")
    rows = list(rows)
    rows = [ {'id':row[0] ,'task':row[1], 'complete':row[2]} for row in rows ]
    completed_list = []
    for x in range(0,len(rows)):
        if rows[x]['complete']== True:
            completed_list.append(rows[x])
    return template("completed_list.tpl", name="sf", completed_list=completed_list)



@route('/regenerate')
def get_regenerate():
    setup_table()
    return redirect('/list')

@route('/edit-list')
def get_edit_list():
    cursor = connection.cursor()
    rows = cursor.execute("select id, task, complete from list")
    rows = list(rows)
    rows = [ {'id':row[0] ,'task':row[1], 'complete':row[2]} for row in rows ]
    return template("edit_list.tpl", name="sf", task_list=rows)

@route('/remove-task/<id>')
def get_remove_item(id):
    cursor = connection.cursor()
    cursor.execute(f"delete from list where id={id}")
    connection.commit()
    redirect('/edit-list')

@post('/add-task')
def post_add():
    new_task = request.forms.get("new_task")
    cursor = connection.cursor()
    cursor.execute(f"insert into list (task, complete) values ('{new_task}', false)")
    connection.commit()
    redirect('/list')
@route('/shared-expenses')
def get_shared_expenses():
    redirect('/')




application = default_app()

