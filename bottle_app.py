from bottle import Bottle, default_app, route, get, post, request, redirect, template, run
from setup import setup_user_list, generate_tasks
from password_manager import generate_password_hash, verify_password_hash
import sqlite3
from datetime import datetime
import pytz


connection = sqlite3.connect("daily_list.db")


@route('/')
def get_index():
    return template('index.tpl')

@route('/tz')
def get_tz():
    return template('timezone.tpl')    

@post('/login')
def get_login():
    user_id = request.forms.get('user_id')
    username = request.forms.get('username')
    typed_pwd = request.forms.get('password')
    timezone = request.forms.get('timezone')
    
    cursor = connection.cursor()
    login_query = list(cursor.execute('select id, password from users where username = ?', (username,)))
    stored_password_hash = login_query[0][1]
    if verify_password_hash(typed_pwd,stored_password_hash):
        print("login successful")
        user_id = login_query[0][0]
        redirect(f'/list/{user_id}?timezone={timezone}')
    else:
        return template('retry')
   

@route('/logout')
def get_logout():
    redirect('/')

@route('/registration')
def get_registration():
    return template('registration')


@post('/register')
def post_register():
    username = request.forms.get('username')
    password_hash = generate_password_hash(request.forms.get('password'))
    timezone = request.forms.get('timezone')
    cursor = connection.cursor()
    insert_user_record = cursor.execute('insert into users (username, password) values (?,?)', (username, password_hash))
    connection.commit()
    rows = list(cursor.execute('select id from users where username = ?', (username,)))
    user_id= rows[0][0]
    setup_user_list(user_id)
    redirect(f'/list/{user_id}?timezone={timezone}')


@route('/list/<user_id>')
def get_list(user_id):
    timezone = request.query.get('timezone')
    cursor = connection.cursor()
    rows = cursor.execute("select * from list where user_id = ?", (user_id,))
    rows = list(rows)
    user_record = list(cursor.execute("select * from users where id = ?", (user_id,)))
    username = user_record[0][1]
    date = datetime.now(tz=pytz.timezone(timezone)).strftime("%Y-%m-%d")
    prev_tasks_date = list(cursor.execute("select max(date_assigned) from tasks where user_id = ?", (user_id,)))
    prev_tasks_date = prev_tasks_date[0][0]
    if prev_tasks_date is None:
        generate_tasks(user_id, timezone)
    elif prev_tasks_date < date:
        generate_tasks(user_id, timezone)
    rows = cursor.execute("select id, user_id, task, date_assigned, completion_status from tasks where user_id = ? and completion_status = false and date_assigned = ?", (user_id, date))
    rows = list(rows)
    rows = [ {'id':row[0] , 'user_id':row[1], 'task':row[2], 'date_assigned':row[3], 'completion_status':row[4]} for row in rows ]
    context = {'user_id': user_id, 'username' : username, 'timezone' : timezone}
    return template("daily_list.tpl", name=username, uncompleted_task_list=rows, context=context, timezone=timezone)


@route('/complete', method='POST')
def get_complete_task():
    id = request.forms.get('id')
    timezone = request.forms.get('timezone')
    user_id = request.forms.get('user_id')
    cursor = connection.cursor()
    cursor.execute("update tasks set completion_status = true where id = ?", (id,))
    connection.commit()
    redirect(f'/list/{user_id}?timezone={timezone}')


@route('/undo-complete', method='POST')
def get_undo_complete_task():
    id = request.forms.get('id')
    user_id = request.forms.get('user_id')
    timezone = request.forms.get('timezone')
    cursor = connection.cursor()
    cursor.execute("update tasks set completion_status = false where id = ?", (id,))
    connection.commit()
    redirect(f'/completed-list/{user_id}?timezone={timezone}')

@route("/completed-list/<user_id>")
def get_complete(user_id):
    cursor = connection.cursor()
    user_record = list(cursor.execute("select * from users where id = ?", (user_id,)))
    username = user_record[0][1]
    timezone = request.query.get('timezone')
    date = datetime.now(tz=pytz.timezone(timezone)).strftime("%Y-%m-%d")
    rows = cursor.execute("select id, user_id, task, date_assigned, completion_status from tasks where user_id = ? and completion_status = true and date_assigned = ?", (user_id, date))
    rows = list(rows)
    rows = [ {'id':row[0], 'user_id':row[1], 'task':row[2], 'date_assigned':row[3], 'completion_status':row[4]} for row in rows ]
    context = {'user_id': user_id, 'username' : username, 'timezone' : timezone}
    return template("completed_list.tpl", name="sf", completed_task_list=rows, context=context)



@route('/regenerate/<user_id>')
def get_regenerate(user_id):
    timezone = request.query.get('timezone')
    generate_tasks(user_id, timezone)
    redirect(f'/list/{user_id}?timezone={timezone}')

@route('/edit-list/<user_id>')
def get_edit_list(user_id):
    cursor = connection.cursor()
    rows = cursor.execute("select id, user_id, task from list where user_id = ?", (user_id,))
    rows = list(rows)
    rows = [ {'id':row[0], 'user_id':row[1], 'task':row[2]} for row in rows ]
    timezone = request.query.get('timezone')
    context = {'user_id': user_id, 'timezone' : timezone}
    return template("edit_list.tpl", name="sf", task_list=rows, context=context)

@post('/remove-task')
def post_remove_item():
    id = request.forms.get("id")
    timezone = request.forms.get('timezone')
    user_id = request.forms.get("user_id")
    cursor = connection.cursor()
    cursor.execute("delete from list where id = ?", (id,))
    connection.commit()
    redirect(f'/edit-list/{user_id}?timezone={timezone}')

@post('/add-task')
def post_add():
    new_task = request.forms.get("new_task")
    user_id = request.forms.get("user_id")
    timezone = request.forms.get("timezone")
    cursor = connection.cursor()
    cursor.execute("insert into list (user_id, task) values (?,?)", (user_id, new_task,))
    connection.commit()
    redirect(f'/edit-list/{user_id}?timezone={timezone}')





#application = default_app()
run(host='localhost', port=8080, application=Bottle())