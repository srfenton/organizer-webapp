from bottle import Bottle, default_app, route, get, post, request, redirect, template
from setup import setup_user, generate_tasks
import sqlite3
from datetime import datetime
import pytz
from bottle_session import Session
import redis


connection = sqlite3.connect("daily_list.db")

# app = Bottle()
plugin = bottle_session.SessionPlugin(cookie_lifetime=600)
app.install(plugin)
session = Session(app)

@route('/')
def get_index():
    return template('index.tpl')

@post('/login')
def get_login():
    user_id = request.forms.get('user_id')
    time_zone = request.forms.get('time_zone')
    print(time_zone+"FINDMEHERE")
    # session["user_id"] = user_id
    # session["time_zone"] = time_zone
    redirect(f'/list/{user_id}')

@route('/logout')
def get_logout():

    redirect('/')

@route('/registration')
def get_registration():
    return template('registration')


@post('/register')
def post_register():
    username = request.forms.get('username')
    password = request.forms.get('password')
    cursor = connection.cursor()
    rows = cursor.execute('insert into users (username, password) values (?,?)', (username, password))
    redirect(f'/list/{user_id}')


@route('/list/<user_id>')
# @route('/list/')
def get_list(user_id):
# def get_list():
    date = datetime.now(tz=pytz.timezone('US/Pacific')).strftime("%Y-%m-%d")
    cursor = connection.cursor()
    # user_id = request.session.get("user_id")
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
    date = datetime.now(tz=pytz.timezone('US/Pacific')).strftime("%Y-%m-%d")
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
def post_remove_item():
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

