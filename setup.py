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
    cursor.execute("insert into list (task, complete) values ('test item', false)")

    # cursor.execute("create table list (id integer primary key, task text, date_completed test)")

    # cursor.execute("insert into list (task) values ('Sunlight')")
    # cursor.execute("insert into list (task) values ('Cold Shower'")
    # cursor.execute("insert into list (task) values ('Exercise')")
    # cursor.execute("insert into list (task) values ('Zazen')")
    # cursor.execute("insert into list (task) values ('Hibiscus')")
    # cursor.execute("insert into list (task) values ('Water I')")
    # cursor.execute("insert into list (task) values ('Water II')")
    # cursor.execute("insert into list (task) values ('Water III')")
    # cursor.execute("insert into list (task) values ('Language Lesson')")
    # cursor.execute("insert into list (task) values ('Science Lesson')")

    connection.commit()
    connection.close()

    print("done.")
