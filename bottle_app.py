from bottle import default_app, route, get, post, request, redirect, template
from setup import setup_table, generate_tasks
import sqlite3
from time import gmtime, strftime


connection = sqlite3.connect("daily_list.db")

@route('/')
def get_index():
    return template("index.tpl")

@post('/login')
def get_login():
    user_id = request.forms.get("user_id")
    redirect(f'/list/{user_id}')


@route('/list/<user_id>')
def get_list(user_id):
    date = str(strftime("%Y %m %d"))
    cursor = connection.cursor()
    rows = cursor.execute("select * from list where user_id = ?", (user_id,))
    rows = list(rows)
    if len(rows) == 0:
       generate_tasks(user_id, connection)
       rows = cursor.execute("select id, user_id, task, date_assigned, completion_status from tasks where user_id = ? and completion_status = false and date_assigned = ?", (user_id, date))
       rows = list(rows)
    else:
        rows = cursor.execute("select id, user_id, task, date_assigned, completion_status from tasks where user_id = ? and completion_status = false and date_assigned = ?", (user_id, date))
        rows = list(rows)
        rows = [ {'id':row[0] , 'user_id':row[1], 'task':row[2], 'date_assigned':row[3], 'completion_status':row[4]} for row in rows ]
    context = {'user_id': user_id}
    return template("daily_list.tpl", name="sf", uncompleted_task_list=rows, context=context)


@route('/complete', method='POST')
def get_complete_task():
    id = request.forms.get('id')
    user_id = request.forms.get('user_id')
    cursor = connection.cursor()
    cursor.execute("update tasks set completion_status = true where id = ?", (id,))
    connection.commit()
    redirect(f'/list/{user_id}')


@route('/undo-complete', method='POST')
def get_undo_complete_task():
    id = request.forms.get('id')
    user_id = request.forms.get('user_id')
    cursor = connection.cursor()
    cursor.execute("update tasks set completion_status = false where id = ?", (id,))
    connection.commit()
    redirect(f'/completed-list/{user_id}')

@route("/completed-list/<user_id>")
def get_complete(user_id):
    date = str(strftime("%Y %m %d"))
    cursor = connection.cursor()
    rows = cursor.execute("select id, user_id, task, date_assigned, completion_status from tasks where user_id = ? and completion_status = true and date_assigned = ?", (user_id, date))
    rows = list(rows)
    rows = [ {'id':row[0], 'user_id':row[1], 'task':row[2], 'date_assigned':row[3], 'completion_status':row[4]} for row in rows ]
    context = {'user_id': user_id}
    return template("completed_list.tpl", name="sf", completed_task_list=rows, context=context)



@route('/regenerate/<user_id>')
def get_regenerate(user_id):
    generate_tasks(user_id)
    return redirect(f'/list/{user_id}')

@route('/edit-list/<user_id>')
def get_edit_list(user_id):
    cursor = connection.cursor()
    rows = cursor.execute("select id, user_id, task from list where user_id = ?", (user_id,))
    rows = list(rows)
    rows = [ {'id':row[0], 'user_id':row[1], 'task':row[2]} for row in rows ]
    context = {'user_id': user_id}
    return template("edit_list.tpl", name="sf", task_list=rows, context=context)

@post('/remove-task')
def get_remove_item():
    id = request.forms.get("id")
    user_id = request.forms.get("user_id")
    cursor = connection.cursor()
    cursor.execute("delete from list where id = ?", (id,))
    connection.commit()
    redirect(f'/edit-list/{user_id}')

@post('/add-task')
def post_add():
    new_task = request.forms.get("new_task")
    user_id = request.forms.get("user_id")
    cursor = connection.cursor()
    cursor.execute("insert into list (user_id, task) values (?,?)", (user_id, new_task,))
    connection.commit()
    redirect(f'/edit-list/{user_id}')





application = default_app()

