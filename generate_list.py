import sqlite3
from time import gmtime, strftime

# DB-API spec for talking to relational databases in Python
#iterate through the items in a table, which are user added tasks and add them into a table with today's date

def generate_table():
    connection = sqlite3.connect('daily_list.db')

    cursor = connection.cursor()
    cursor.execute('select * from list;')
    date = str(strftime("%Y %m %d"))
    records = [row[0] for row in cursor.fetchall()]

    for x in records:
        cursor.execute('insert into tasks (task, date_assigned, completion_status) values (?,?, false)', (x, date))

    connection.commit()
    connection.close()

    print('done.')
