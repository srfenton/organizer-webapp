from bottle import Bottle, default_app, route, get, post, response, request, redirect, template, run, error
from setup import setup_user_list, generate_tasks
from password_manager import generate_password_hash, verify_password_hash, is_valid_password
from generate_stats import generate_main_table
from datetime import datetime, date, timedelta
from session_manager import random_id, validate_session
import sqlite3
import pytz
import calendar


connection = sqlite3.connect("daily_list.db")


@route('/')
def get_index():
    session_id = request.get_cookie("session_id")
    if not session_id:
        session_id = random_id()
        response.set_cookie("session_id", session_id)
    return template('index.tpl')    

@route('/tz')
def get_tz():
    return template('timezone.tpl')    

@route('/graphs')
def get_graphs():
    return template('graphs.tpl')    


@post('/login')
def get_login():
    username = request.forms.get('username')
    #the username should be case insensitive and free of white space
    username = username.lower().strip()
    typed_pwd = request.forms.get('password')
    timezone = request.forms.get('timezone')
    response.set_cookie("timezone", timezone)
    
    if not username or not typed_pwd:
        return template('retry')

    cursor = connection.cursor()
    cursor.execute('SELECT id, password, username FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    
    if user is None:
        return template('retry')

    user_id, stored_password_hash, stored_username = user
    
    if verify_password_hash(typed_pwd, stored_password_hash):
        print("login successful")
        session_id = request.get_cookie("session_id")
         # Check if the session_id already exists
        cursor.execute('SELECT * FROM sessions WHERE session_id = ?', (session_id,))
        existing_session = cursor.fetchone()
        if existing_session:
            # If session_id exists, update it or handle appropriately
            print("Session already exists, skipping insertion")
        else:
            cursor.execute('INSERT INTO sessions (user_id, session_id) VALUES (?, ?)', (user_id, session_id))
            connection.commit()
            print('saving session_id')

        response.set_cookie("user_id", str(user_id))
        redirect(f'/list/{user_id}')

    else:
        return template('retry')

   

@route('/logout')
def get_logout():
    response.delete_cookie('session_id')
    response.delete_cookie('user_id')
    redirect('/')

@route('/registration')
def get_registration():
    return template('registration')


@post('/register')
def post_register():
    session_id = request.get_cookie("session_id")
    if not session_id:
        session_id = random_id()
        response.set_cookie("session_id", session_id)
    cursor = connection.cursor()
    username = request.forms.get('username')
    #the username should be case insensitive and free of white space
    username = username.lower().strip() 
    password_unhashed = request.forms.get('password')
    password_confirmation = request.forms.get('password_confirmation')
    if username == '' or username is None:
        return template('registration')

    check_username_in_database_result = cursor.execute('select * from users where username = ?', (username,))
    user = cursor.fetchone()
    print(f'{user} is user')
    if user != None:
        return template('registration')
    if is_valid_password(password_unhashed, password_confirmation) == False:
        print(f'{is_valid_password(password_unhashed, password_confirmation) == False} is the password validator')
        return template('registration')
    password_hash = generate_password_hash(password_unhashed)
    timezone = request.forms.get('timezone')
    response.set_cookie('timezone', timezone)
    insert_user_record = cursor.execute('insert into users (username, password) values (?,?)', (username, password_hash))
    connection.commit()
    rows = list(cursor.execute('select id from users where username = ?', (username,)))
    user_id= rows[0][0]
    setup_user_list(user_id)
    cursor.execute('insert into sessions (user_id, session_id) values (?,?)', (user_id, session_id))
    connection.commit()
    response.set_cookie("user_id", str(user_id))
    redirect(f'/list/{user_id}')



@route('/list/<user_id>')
def get_list(user_id):
    print(user_id)
    session_id = request.get_cookie('session_id')
    # Validate the session before proceeding
    if not validate_session(session_id, user_id):
        redirect('/')  # Redirect to login page if session is invalid
    
    timezone = request.get_cookie('timezone')
    cursor = connection.cursor()
    rows = cursor.execute("select * from list where user_id = ?", (user_id,))
    rows = list(rows)
    user_record = list(cursor.execute("select * from users where id = ?", (user_id,)))
    username = user_record[0][1]
    
    selected_date = request.query.get('date', 'today')
    if selected_date == 'yesterday':
        yesterday = datetime.now(tz=pytz.timezone(timezone)) - timedelta(days = 1)
        date = yesterday.strftime("%Y-%m-%d") 
    else:
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
    context = {'user_id': user_id, 'username' : username, 'timezone' : timezone, 'date' : date }

    return template("daily_list.tpl", name=username, uncompleted_task_list=rows, context=context, timezone=timezone)


@route('/complete', method='POST')
def get_complete_task():
    session_id = request.get_cookie("session_id")
    user_id = request.get_cookie('user_id')

    # Validate the session before proceeding
    if not validate_session(session_id, user_id):
        redirect('/')  # Redirect to login page if session is invalid
    id = request.forms.get('id')
    timezone = request.get_cookie('timezone')
    user_id = request.forms.get('user_id')
    cursor = connection.cursor()
    cursor.execute("update tasks set completion_status = true where id = ?", (id,))
    connection.commit()
    print('complete action was successful')
    redirect(f'/list/{user_id}')


@route('/undo-complete', method='POST')
def get_undo_complete_task():
    session_id = request.get_cookie('session_id')
    user_id = request.get_cookie('user_id')
    
    # Validate the session before proceeding
    if not validate_session(session_id, user_id):
        redirect('/')  # Redirect to login page if session is invalid
    id = request.forms.get('id')
    user_id = request.forms.get('user_id')
    timezone = request.get_cookie('timezone')
    cursor = connection.cursor()
    cursor.execute("update tasks set completion_status = false where id = ?", (id,))
    connection.commit()
    redirect(f'/completed-list/{user_id}')

@route("/completed-list/<user_id>")
def get_complete(user_id):
    session_id = request.get_cookie('session_id') 
    
    # Validate the session before proceeding
    if not validate_session(session_id, user_id):
        redirect('/')  # Redirect to login page if session is invalid
    cursor = connection.cursor()
    user_record = list(cursor.execute("select * from users where id = ?", (user_id,)))
    username = user_record[0][1]
    timezone = request.get_cookie('timezone')
    selected_date = request.query.get('date', 'today')
    if selected_date == 'yesterday':
        yesterday = datetime.now(tz=pytz.timezone(timezone)) - timedelta(days = 1)
        date = yesterday.strftime("%Y-%m-%d") 
    else:
        date = datetime.now(tz=pytz.timezone(timezone)).strftime("%Y-%m-%d")
    rows = cursor.execute("select id, user_id, task, date_assigned, completion_status from tasks where user_id = ? and completion_status = true and date_assigned = ?", (user_id, date))
    rows = list(rows)
    rows = [ {'id':row[0], 'user_id':row[1], 'task':row[2], 'date_assigned':row[3], 'completion_status':row[4]} for row in rows ]
    context = {'user_id': user_id, 'username' : username, 'timezone' : timezone}

    return template("completed_list.tpl", name="sf", completed_task_list=rows, context=context)


@route('/edit-list/<user_id>')
def get_edit_list(user_id):
    session_id = request.get_cookie("session_id")
    user_id = request.get_cookie('user_id')

    
    # Validate the session before proceeding
    if not validate_session(session_id, user_id):
        redirect('/')  # Redirect to login page if session is invalid
    cursor = connection.cursor()
    cursor.execute("select id, user_id, task from list where user_id = ?", (user_id,))
    rows = cursor.fetchall()
    if not rows:
        return template('add_item.tpl')
    
    rows = [ {'id':row[0], 'user_id':row[1], 'task':row[2]} for row in rows ]
    timezone = request.get_cookie('timezone')
    context = {'user_id': user_id, 'timezone' : timezone}
    return template("edit_list.tpl", task_list=rows, context=context)

@post('/remove-task')
def post_remove_item():
    session_id = request.get_cookie("session_id")
    user_id = request.get_cookie('user_id')
    
    # Validate the session before proceeding
    if not validate_session(session_id, user_id):
        redirect('/')  # Redirect to login page if session is invalid
    id = request.forms.get("id")
    timezone = request.get_cookie('timezone')
    cursor = connection.cursor()
    rows = list(cursor.execute('select task from list where id = ?', (id,)))
    task = rows[0][0]
    cursor.execute("delete from list where id = ?", (id,))
    cursor.execute("delete from tasks where task = ? and user_id = ?", (task, user_id))
    connection.commit()
    redirect(f'/edit-list/{user_id}')

@post('/add-task')
def post_add():
    session_id = request.get_cookie("session_id")
    user_id = request.get_cookie('user_id')
    
    # Validate the session before proceeding
    if not validate_session(session_id, user_id):
        redirect('/')  # Redirect to login page if session is invalid
    new_task = request.forms.get("new_task")
    timezone = request.get_cookie("timezone")
    cursor = connection.cursor()
    cursor.execute("insert into list (user_id, task) values (?,?)", (user_id, new_task,))
    connection.commit()
    generate_tasks(user_id, timezone)
    redirect(f'/edit-list/{user_id}')


@get('/stats/<user_id>')
def get_stats(user_id):
    session_id = request.get_cookie("session_id")
    
    # Validate the session before proceeding
    if not validate_session(session_id, user_id):
        redirect('/')  # Redirect to login page if session is invalid
    cursor = connection.cursor()
    user_record = list(cursor.execute("select * from users where id = ?", (user_id,)))
    username = user_record[0][1]
    rows = generate_main_table(user_id)
    timezone = request.get_cookie('timezone')
    current_month = datetime.now().month
    one_month_ago = (current_month - 2) % 12 + 1  # Wraps around to December if needed
    two_months_ago = (current_month - 3) % 12 + 1  # Wraps around to November if needed
    one_month_string = calendar.month_name[one_month_ago]  # Get month name
    two_months_string = calendar.month_name[two_months_ago]  # Get month name
    print(f'{one_month_string} IS ONE MONTH')
    context = {'user_id': user_id, 'username' : username, 'timezone' : timezone, 'one_month_string' : one_month_string,'two_months_string' : two_months_string}
    return template("stats.tpl", name=username, stats_list=rows, context=context)

#####################################################################################################################
#UNDER CONSTRUCTION
#####################################################################################################################

@route("/account/<user_id>")
def get_account(user_id):
    session_id = request.get_cookie('session_id') 

    # Validate the session before proceeding
    if not validate_session(session_id, user_id):
        redirect('/')  # Redirect to login page if session is invalid
    cursor = connection.cursor()
    user_record = list(cursor.execute("select * from users where id = ?", (user_id,)))
    username = user_record[0][1]
    timezone = request.get_cookie('timezone')
    date = datetime.now(tz=pytz.timezone(timezone)).strftime("%Y-%m-%d")
    rows = cursor.execute("select id, user_id, task, date_assigned, completion_status from tasks where user_id = ? and completion_status = true and date_assigned = ?", (user_id, date))
    rows = list(rows)
    rows = [ {'id':row[0], 'user_id':row[1], 'task':row[2], 'date_assigned':row[3], 'completion_status':row[4]} for row in rows ]
    context = {'user_id': user_id, 'username' : username, 'timezone' : timezone}
    return template("account.tpl", completed_task_list=rows, context=context)

@route("/account/vacations/<user_id>")
def get_vacations(user_id):
    session_id = request.get_cookie('session_id') 

    # Validate the session before proceeding
    if not validate_session(session_id, user_id):
        redirect('/')  # Redirect to login page if session is invalid
    cursor = connection.cursor()
    user_record = list(cursor.execute("select * from users where id = ?", (user_id,)))
    username = user_record[0][1]
    timezone = request.get_cookie('timezone')
    date = datetime.now(tz=pytz.timezone(timezone)).strftime("%Y-%m-%d")
    rows = cursor.execute("select id, user_id, vacation_date from vacations where user_id = ? order by vacation_date desc", (user_id,))
    rows = list(rows)
    rows = [ {'id':row[0], 'user_id':row[1], 'vacation_date':row[2]} for row in rows ]
    context = {'user_id': user_id, 'username' : username, 'timezone' : timezone}
    return template("vacations.tpl", vacation_days_list=rows, context=context)

@route('/delete-vacation', method='POST')
def post_delete_vacation():
    session_id = request.get_cookie('session_id')
    user_id = request.get_cookie('user_id')
    
    # Validate the session before proceeding
    if not validate_session(session_id, user_id):
        redirect('/')  # Redirect to login page if session is invalid
    id = request.forms.get('id')
    user_id = request.forms.get('user_id')
    timezone = request.get_cookie('timezone')
    cursor = connection.cursor()
    cursor.execute("delete from vacations where id = ?", (id,))
    connection.commit()
    redirect(f'/account/vacations/{user_id}')

@route('/add-vacation', method='POST')
def post_add_vacation():
    session_id = request.get_cookie('session_id')
    user_id = request.get_cookie('user_id')
    
    # Validate the session before proceeding
    if not validate_session(session_id, user_id):
        redirect('/')  # Redirect to login page if session is invalid
    # id = request.forms.get('id')
    date = request.forms.get('date')
    user_id = request.forms.get('user_id')
    timezone = request.get_cookie('timezone')
    cursor = connection.cursor()
    cursor.execute("insert into vacations(user_id, vacation_date) values(?,?) ", (user_id, date))
    connection.commit()
    redirect(f'/account/vacations/{user_id}')

#####################################################################################################################
#UNDER CONSTRUCTION
#####################################################################################################################

#application = default_app()
run(host='localhost', port=8080, application=Bottle(), debug=True, reloader=True)