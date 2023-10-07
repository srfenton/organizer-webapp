import sqlite3

# DB-API spec for talking to relational databases in Python
def generate_table():
    connection = sqlite3.connect("daily_list.db")

    cursor = connection.cursor()

    try:
        cursor.execute("drop table list")
    except:
        pass

    cursor.execute("create table list (id integer primary key, task text, date_completed test)")

    cursor.execute("insert into list (task) values ('Sunlight')")
    cursor.execute("insert into list (task) values ('Cold Shower'")
    cursor.execute("insert into list (task) values ('Exercise')")
    cursor.execute("insert into list (task) values ('Zazen')")
    cursor.execute("insert into list (task) values ('Hibiscus')")
    cursor.execute("insert into list (task) values ('Water I')")
    cursor.execute("insert into list (task) values ('Water II')")
    cursor.execute("insert into list (task) values ('Water III')")
    cursor.execute("insert into list (task) values ('Language Lesson')")
    cursor.execute("insert into list (task) values ('Science Lesson')")

    connection.commit()
    connection.close()

    print("done.")
