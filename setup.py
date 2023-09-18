import sqlite3

# DB-API spec for talking to relational databases in Python
def setup_table():
    connection = sqlite3.connect("daily_list.db")

    cursor = connection.cursor()

    try:
        cursor.execute("drop table list")
    except:
        pass

    cursor.execute("create table list (id integer primary key, task text, complete boolean)")

    cursor.execute("insert into list (task, complete) values ('sunlight', false)")
    cursor.execute("insert into list (task, complete) values ('cold shower', false)")
    cursor.execute("insert into list (task, complete) values ('exercise', false)")
    cursor.execute("insert into list (task, complete) values ('zazen', false)")
    cursor.execute("insert into list (task, complete) values ('hibiscus', false)")
    cursor.execute("insert into list (task, complete) values ('water i', false)")
    cursor.execute("insert into list (task, complete) values ('water ii', false)")
    cursor.execute("insert into list (task, complete) values ('water iii', false)")
    cursor.execute("insert into list (task, complete) values ('language lesson', false)")
    cursor.execute("insert into list (task, complete) values ('physics lesson', false)")

    connection.commit()
    connection.close()

    print("done.")
