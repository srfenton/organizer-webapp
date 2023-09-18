import sqlite3
connection = sqlite3.connect("daily_list.db")
cursor = connection.cursor()
rows = cursor.execute("select id, task, complete from list")
rows = list(rows)
rows = [ {'id':row[0] ,'task':row[1], 'complete':row[2]} for row in rows ]
completed_list = []
for x in range(0,len(rows)):
    print(rows[x])
    if rows[x]['complete']== True:
        completed_list.append(rows[x])
print(completed_list)