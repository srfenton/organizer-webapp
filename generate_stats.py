import sqlite3


connection = sqlite3.connect('daily_list.db')


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


if __name__ == '__main__':
    print(generate_total_percentages(1))
    print(generate_current_month(1))
    print('done...')
    
