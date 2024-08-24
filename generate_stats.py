import sqlite3


connection = sqlite3.connect('daily_list.db')

#ideally, instead of several different tables, as many of these functions as possible should generate a dictionary with their task as key and result as the value. That way, they can be aggregated to a single table.
def generate_total_percentages(user_id,connection=None):
    if connection is None:
        connection = sqlite3.connect("daily_list.db")
    cursor = connection.cursor()
    total_percentages = cursor.execute('''
        SELECT 
            l.task, 
            COALESCE(completed_tasks.completed_tasks, 0) AS complete_task_count,
            COALESCE(days_assigned.days_assigned, 0) AS days_assigned_count,
            printf("%.2f%%", COALESCE(completed_tasks.completed_tasks, 0) * 100.0 / COALESCE(days_assigned.days_assigned, 1)) AS percentage
        
        FROM 
            list l
            
        LEFT JOIN 
            (SELECT task, COUNT(*) AS completed_tasks 
            FROM tasks 
            WHERE user_id = ? AND completion_status = true 
            GROUP BY task) AS completed_tasks
        ON 
            l.task = completed_tasks.task
            
        LEFT JOIN
            (select task, (JULIANDAY(DATE('now')) - JULIANDAY(MIN(date_assigned))) AS days_assigned
            from tasks 
            where user_id = ?
            group by task) as days_assigned
        ON
            l.task = days_assigned.task

        WHERE
            l.user_id = ?
        ORDER BY percentage desc;
            
                        
                            
        ''', (user_id,user_id,user_id,))
    rows = list(total_percentages)

    return rows

def generate_total_percentages(user_id,connection=None):
    if connection is None:
        connection = sqlite3.connect("daily_list.db")
    cursor = connection.cursor()
    total_percentages = cursor.execute('''
        SELECT 
            l.task, 
            COALESCE(completed_tasks.completed_tasks, 0) AS complete_task_count,
            COALESCE(days_assigned.days_assigned, 0) AS days_assigned_count,
            printf("%.2f%%", COALESCE(completed_tasks.completed_tasks, 0) * 100.0 / COALESCE(days_assigned.days_assigned, 1)) AS percentage
        
        FROM 
            list l
            
        LEFT JOIN 
            (SELECT task, COUNT(*) AS completed_tasks 
            FROM tasks 
            WHERE user_id = ? AND completion_status = true 
            GROUP BY task) AS completed_tasks
        ON 
            l.task = completed_tasks.task
            
        LEFT JOIN
            (select task, (JULIANDAY(DATE('now')) - JULIANDAY(MIN(date_assigned)) + 1) AS days_assigned
            from tasks 
            where user_id = ?
            group by task) as days_assigned
        ON
            l.task = days_assigned.task

        WHERE
            l.user_id = ?
        ORDER BY percentage desc;
            
                        
                            
        ''', (user_id,user_id,user_id,))
    rows = list(total_percentages)

    return rows


def generate_current_month(user_id,connection=None):
    if connection is None:
        connection = sqlite3.connect("daily_list.db")
    cursor = connection.cursor()
    total_percentages = cursor.execute('''
        WITH days_assigned AS (
    SELECT COUNT(*) AS days_assigned
    FROM tasks 
    WHERE user_id = ? 
    AND date_assigned BETWEEN DATE('now', 'start of month') AND DATE('now')
)

SELECT 
    l.task, 
    COALESCE(completed_tasks.completed_tasks, 0) AS complete_task_count,
    days_assigned.days_assigned AS days_assigned_count,
    printf("%.2f%%", COALESCE(completed_tasks.completed_tasks, 0) * 100.0 / COALESCE(days_assigned.days_assigned, 1)) AS percentage
    
FROM 
    list l
    
LEFT JOIN 
    (SELECT task, COUNT(*) AS completed_tasks 
     FROM tasks 
     WHERE user_id = ? AND completion_status = true 
     AND date_assigned BETWEEN DATE('now', 'start of month') AND DATE('now')
     GROUP BY task) AS completed_tasks
ON 
    l.task = completed_tasks.task

CROSS JOIN 
    days_assigned

WHERE
    l.user_id = ?;

            
                        
                            
        ''', (user_id,user_id,user_id,))
    rows = list(total_percentages)

    return rows

#this function takes a list of tuples as its argument generated from sqlite with each task in index 0 of the tuple and the aggregated value in index 3 
def generate_stats_table(current_month, total_percentages):
    stats_table = {}
    #create a dict for each task and a nested dict total and current month values
    for x in total_percentages:
        stats_table.update({x[0] : [{'total' : x[3]}]}) 
    for x in current_month:
        stats_table[x[0]].append({'current month':x[3]})
    
    return stats_table

if __name__ == '__main__':
    current_month = generate_current_month(1)
    total_percentages = generate_total_percentages(1)
    # print(current_month)
    # print(total_percentages)
    generate_stats_table(current_month, total_percentages)
    print('done...')
    
