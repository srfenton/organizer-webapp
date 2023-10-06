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

    cursor.execute("insert into list (task, complete) values ('Sunlight', false)")
    cursor.execute("insert into list (task, complete) values ('Cold Shower', false)")
    cursor.execute("insert into list (task, complete) values ('Exercise', false)")
    cursor.execute("insert into list (task, complete) values ('Zazen', false)")
    cursor.execute("insert into list (task, complete) values ('Hibiscus', false)")
    cursor.execute("insert into list (task, complete) values ('Water I', false)")
    cursor.execute("insert into list (task, complete) values ('Water II', false)")
    cursor.execute("insert into list (task, complete) values ('Water III', false)")
    cursor.execute("insert into list (task, complete) values ('Language Lesson', false)")
    cursor.execute("insert into list (task, complete) values ('Science Lesson', false)")

    connection.commit()
    connection.close()

    print("done.")
