import sqlite3
from time import gmtime, strftime


connection = sqlite3.connect('daily_list.db')

def setup_table(user_id,connection=None):
    if connection is None:
        connection = sqlite3.connect("daily_list.db")
    cursor = connection.cursor()

    try:
        cursor.execute("drop table list")
    except:
        pass

    cursor.execute("create table list (id integer primary key, user_id integer, task text)")

    # cursor.execute("insert into list (task) values ('Sunlight')")
    # cursor.execute("insert into list (task) values ('Cold Shower')")
    # cursor.execute("insert into list (task) values ('Exercise')")
    # cursor.execute("insert into list (task) values ('Zazen')")
    # cursor.execute("insert into list (task) values ('Hibiscus')")
    # cursor.execute("insert into list (task) values ('Water I')")
    # cursor.execute("insert into list (task) values ('Water II')")
    # cursor.execute("insert into list (task) values ('Water III')")
    # cursor.execute("insert into list (task) values ('Language Lesson')")
    # cursor.execute("insert into list (task) values ('Science Lesson')")
    cursor.execute("insert into list (task, user_id) values ('get some sunlight into your eyes', ?)", (user_id,))
    cursor.execute("insert into list (task, user_id) values ('reach out to a friend', ?)", (user_id,))
    cursor.execute("insert into list (task, user_id) values ('hydrate', ?)", (user_id,))
    cursor.execute("insert into list (task, user_id) values ('go for a walk', ?)", (user_id,))
    cursor.execute("insert into list (task, user_id) values ('do some light reading', ?)", (user_id,))
    cursor.execute("insert into list (task, user_id) values ('write your end of day thoughts into a journal before bed so you can get some deep, restful sleep', ?)", (user_id,))

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

def generate_tasks(user_id, connection=None):
    if connection is None:
        connection = sqlite3.connect("daily_list.db")
    date = str(strftime("%Y %m %d"))
    cursor = connection.cursor()
    cursor.execute('select id, user_id, task from list where user_id = ?;', (user_id,))

    rows = [(row[0],row[1], row[2]) for row in cursor.fetchall()]
    for x in rows:
        cursor.execute('insert into tasks (user_id, task, date_assigned, completion_status) values (?, ?, ?, false)', (x[1], x[2], date))

    connection.commit()


    print('done.')

connection.close()
