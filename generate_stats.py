import sqlite3


connection = sqlite3.connect('daily_list.db')


#this new query combines the total, current month and adds previous month stats in one transaction.
def generate_main_table(user_id,connection=None):
    if connection is None:
        connection = sqlite3.connect("daily_list.db")
    cursor = connection.cursor()
    main_table = cursor.execute('''
    WITH current_month AS (
        SELECT task,
            CASE
                -- If the task was assigned before the current month, count from the first day of the month
                WHEN MIN(date_assigned) < DATE('now', 'start of month') 
                THEN JULIANDAY(DATE('now')) - JULIANDAY(DATE('now', 'start of month')) + 1
                
                -- Otherwise, count from the day the task was first assigned this month
                ELSE JULIANDAY(DATE('now')) - JULIANDAY(MIN(date_assigned)) + 1
                
            END AS days_assigned
        FROM tasks 
        WHERE user_id = ?
        GROUP BY task
    ),

    previous_month AS (
        SELECT task,
            CASE
               -- If the task was assigned before the start of the previous month, count all days of the previous month
               WHEN MIN(date_assigned) < DATE('now', 'start of month', '-1 month') 
               THEN JULIANDAY(DATE('now', 'start of month')) - JULIANDAY(DATE('now', 'start of month', '-1 month')) 
               
               -- Otherwise, count from the date the task was first assigned within the previous month
               ELSE JULIANDAY(DATE('now', 'start of month')) - JULIANDAY(MIN(date_assigned)) 
               
           END AS days_assigned
        FROM tasks 
        WHERE user_id = ?
        AND date_assigned BETWEEN DATE('now', 'start of month', '-1 month') AND DATE('now', 'start of month', '-1 day')
        GROUP BY task
    )

    SELECT 
        l.task,     
        printf("%.2f%%", COALESCE(current_month_completed_tasks.completed_tasks, 0) * 100.0 / COALESCE(current_month.days_assigned, 1)) AS current_month_percentage,
        printf("%.2f%%", COALESCE(previous_month_completed_tasks.completed_tasks, 0) * 100.0 / COALESCE(previous_month.days_assigned, 1)) AS previous_month_percentage,
        printf("%.2f%%", COALESCE(total_completed_tasks.completed_tasks, 0) * 100.0 / COALESCE(days_assigned.days_assigned, 1)) AS total_percentage,
        --COALESCE(current_month.days_assigned, 0) AS current_month_days_assigned,
        --COALESCE(previous_month.days_assigned, 0) AS previous_month_days_assigned,
        COALESCE(days_assigned.days_assigned, 0) AS total_days_assigned
        
        
    FROM 
        list l
        
    -- Completed tasks for previous month
    LEFT JOIN 
        (SELECT task, COUNT(*) AS completed_tasks 
        FROM tasks 
        WHERE user_id = ? AND completion_status = true 
        AND date_assigned BETWEEN DATE('now', 'start of month', '-1 month') AND DATE('now', 'start of month', '-1 day')
        GROUP BY task) AS previous_month_completed_tasks
    ON 
        l.task = previous_month_completed_tasks.task
        
    -- Completed tasks for current month
    LEFT JOIN 
        (SELECT task, COUNT(*) AS completed_tasks
        FROM tasks 
        WHERE user_id = ? AND completion_status = true 
        AND date_assigned BETWEEN DATE('now', 'start of month') AND DATE('now')
        GROUP BY task) AS current_month_completed_tasks
    ON 
        l.task = current_month_completed_tasks.task    
        
    -- Total completed tasks
    LEFT JOIN 
        (SELECT task, COUNT(*) AS completed_tasks 
        FROM tasks 
        WHERE user_id = ? AND completion_status = true 
        GROUP BY task) AS total_completed_tasks
    ON 
        l.task = total_completed_tasks.task
        
    -- Days assigned for current month
    LEFT JOIN current_month 
    ON l.task = current_month.task

    -- Days assigned for previous month
    LEFT JOIN previous_month 
    ON l.task = previous_month.task

    --Days assigned total
    LEFT JOIN
        (select task, (JULIANDAY(DATE('now')) - JULIANDAY(MIN(date_assigned))+1) AS days_assigned
        from tasks 
        where user_id = ?
        group by task) as days_assigned
    ON
        l.task = days_assigned.task

    WHERE l.user_id = ?
    ORDER BY COALESCE(current_month_completed_tasks.completed_tasks, 0) * 100.0 / COALESCE(current_month.days_assigned, 1) DESC;
                            
        ''', (user_id,user_id,user_id,user_id,user_id,user_id,user_id,))
    stats_list = [ {'task':row[0], 'current month':row[1],'previous month':row[2], 'total percentage':row[3], 'days assigned count':int(row[4])} for row in main_table]
    rows = list(stats_list)

    return rows

if __name__ == '__main__':
    main_table = generate_main_table(3)
    print(main_table)
    print('done...')
    

