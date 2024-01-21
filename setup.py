import sqlite3
from datetime import datetime
import pytz

connection = sqlite3.connect('daily_list.db')

def setup_db():
    pass


def setup_user(user_id=None,connection=None):
    if connection is None:
        connection = sqlite3.connect("daily_list.db")
    cursor = connection.cursor()
    try:
        cursor.execute("delete from list where user_id = ?", (user_id,))
        cursor.execute("delete from tasks where user_id = ?", (user_id,))
    except:
        pass


    cursor.execute("insert into list (task, user_id) values ('get some sunlight into your eyes', ?)", (user_id,))
    cursor.execute("insert into list (task, user_id) values ('reach out to a friend', ?)", (user_id,))
    cursor.execute("insert into list (task, user_id) values ('hydrate', ?)", (user_id,))
    cursor.execute("insert into list (task, user_id) values ('go for a walk', ?)", (user_id,))
    cursor.execute("insert into list (task, user_id) values ('do some light reading', ?)", (user_id,))
    cursor.execute("insert into list (task, user_id) values ('write your end of day thoughts into a journal before bed so you can get some deep, restful sleep', ?)", (user_id,))

    connection.commit()
    print("done.")

def setup_user_list(user_id,connection=None):
    if connection is None:
        connection = sqlite3.connect("daily_list.db")
    cursor = connection.cursor()
    try:
        cursor.execute("delete from list where user_id = ?", (user_id,))
        cursor.execute("delete from tasks where user_id = ?", (user_id,))
    except:
        pass


    cursor.execute("insert into list (task, user_id) values ('get some sunlight into your eyes', ?)", (user_id,))
    cursor.execute("insert into list (task, user_id) values ('reach out to a friend', ?)", (user_id,))
    cursor.execute("insert into list (task, user_id) values ('hydrate', ?)", (user_id,))
    cursor.execute("insert into list (task, user_id) values ('go for a walk', ?)", (user_id,))
    cursor.execute("insert into list (task, user_id) values ('do some light reading', ?)", (user_id,))
    cursor.execute("insert into list (task, user_id) values ('write your end of day thoughts into a journal before bed so you can get some deep, restful sleep', ?)", (user_id,))

    connection.commit()
    print("done.")

def setup_sf(connection=None):
    if connection is None:
        connection = sqlite3.connect("daily_list.db")
    cursor = connection.cursor()
    user_id = 1
    try:
        cursor.execute("delete from list where user_id = ?", (user_id,))
        cursor.execute("delete from tasks where user_id = ?", (user_id,))
    except:
        pass

    cursor.execute("insert into list (task, user_id) values ('Sunlight', ?)", (user_id,))
    cursor.execute("insert into list (task, user_id) values ('Cold Shower', ?)", (user_id,))
    cursor.execute("insert into list (task, user_id) values ('Exercise', ?)", (user_id,))
    cursor.execute("insert into list (task, user_id) values ('Water I', ?)", (user_id,))
    cursor.execute("insert into list (task, user_id) values ('Water II', ?)", (user_id,))
    cursor.execute("insert into list (task, user_id) values ('Water III', ?)", (user_id,))
    cursor.execute("insert into list (task, user_id) values ('Language Lesson', ?)", (user_id,))
    cursor.execute("insert into list (task, user_id) values ('Science Lesson', ?)", (user_id,))
    cursor.execute("insert into list (task, user_id) values ('Zazen', ?)", (user_id,))
    cursor.execute("insert into list (task, user_id) values ('Journaling', ?)", (user_id,))
    cursor.execute("insert into list (task, user_id) values ('Provide Encouragement', ?)", (user_id,))

    connection.commit()
    print("done.")

def regenerate_tasks_table(connection=None):
    if connection is None:
        connection = sqlite3.connect("daily_list.db")
    cursor = connection.cursor()

    try:
        cursor.execute("drop table tasks")
    except:
        pass

    cursor.execute("create table tasks (id integer primary key, user_id integer, task text, date_assigned text, completion_status boolean)")

    connection.commit()

    print("done.")

def generate_tasks(user_id, user_timezone, connection=None):
    if connection is None:
        connection = sqlite3.connect("daily_list.db")
    date = datetime.now(tz=pytz.timezone(user_timezone)).strftime("%Y-%m-%d")
    cursor = connection.cursor()
    cursor.execute('select id, user_id, task from list where user_id = ?;', (user_id,))

    rows = [(row[0],row[1], row[2]) for row in cursor.fetchall()]
    for x in rows:
        #add a conditional to check for duplicates
        cursor.execute('insert into tasks (user_id, task, date_assigned, completion_status) values (?, ?, ?, false)', (x[1], x[2], date))

    connection.commit()


    print('done.')

connection.close()
