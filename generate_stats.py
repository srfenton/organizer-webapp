import sqlite3


connection = sqlite3.connect('daily_list.db')


def generate_main_table(user_id,connection=None):
    if connection is None:
        connection = sqlite3.connect("daily_list.db")
    cursor = connection.cursor()
    main_table = cursor.execute('''
    WITH current_month AS (
        SELECT 
            t.task,
            CASE
                -- If the task was assigned before the current month, calculate days from the start of the current month to today, excluding vacations
                WHEN MIN(t.date_assigned) < DATE('now', 'start of month') 
                THEN 
                    (JULIANDAY(DATE('now')) - JULIANDAY(DATE('now', 'start of month')) + 1) 
                    - (
                        SELECT COUNT(*) 
                        FROM vacations v 
                        WHERE v.user_id = t.user_id 
                        AND v.vacation_date BETWEEN DATE('now', 'start of month') AND DATE('now')
                    )
                
                -- If the task was assigned during the current month, calculate days from the assignment date to today, excluding vacations
                ELSE 
                    (JULIANDAY(DATE('now')) - JULIANDAY(MIN(t.date_assigned)) + 1) 
                    - (
                        SELECT COUNT(*) 
                        FROM vacations v 
                        WHERE v.user_id = t.user_id 
                        AND v.vacation_date BETWEEN MIN(t.date_assigned) AND DATE('now')
                    )
            END AS days_assigned
        FROM tasks t
        LEFT JOIN vacations v ON v.user_id = t.user_id
        WHERE t.user_id = ?
        GROUP BY t.task

    ),
    previous_month as (
        SELECT 
            t.task,
            CASE 
                -- If the task was assigned before the start of the previous month, count days between assignment and the end of the previous month
                WHEN MIN(t.date_assigned) < DATE('now', 'start of month', '-1 month') 
                THEN (JULIANDAY(DATE('now', 'start of month')) - JULIANDAY(DATE('now', 'start of month', '-1 month'))) - (select count(*) from vacations where user_id = ? and vacation_date between DATE('now', 'start of month', '-1 month') and DATE('now', 'start of month'))
                
                
                -- Otherwise, calculate days between assignment and end of the previous month excluding vacation days before the task was first assigned
                ELSE (
                    JULIANDAY(DATE('now', 'start of month')) - JULIANDAY(MIN(t.date_assigned))
                ) - (
                    SELECT COUNT(*) 
                    FROM vacations v 
                    WHERE v.user_id = t.user_id 
                    AND v.vacation_date BETWEEN MIN(t.date_assigned) AND DATE('now', 'start of month')
                )
            END AS days_assigned
        FROM tasks t
        LEFT JOIN vacations v ON v.user_id = t.user_id
        WHERE t.user_id = ?
        GROUP BY t.task
    ),

    two_month as(
    SELECT 
        t.task,
        CASE 
            -- If the task was assigned after the end of the month two months ago, days assigned should be 0
            WHEN MIN(t.date_assigned) > DATE('now', 'start of month', '-1 month') 
            THEN 0
            
            -- If the task was assigned before the start of two months ago, count days between assignment and the end of two months ago minus vacation days
            WHEN MIN(t.date_assigned) < DATE('now', 'start of month', '-2 months') 
            THEN 
                (
                    JULIANDAY(DATE('now', 'start of month', '-1 month')) 
                    - JULIANDAY(DATE('now', 'start of month', '-2 months'))
                ) 
                - (
                    SELECT COUNT(*) 
                    FROM vacations 
                    WHERE user_id = t.user_id 
                    AND vacation_date BETWEEN DATE('now', 'start of month', '-2 months') 
                                        AND DATE('now', 'start of month', '-1 month')
                )
            
            -- Otherwise, calculate days between assignment and end of the previous month excluding vacation days
            ELSE 
                (
                    JULIANDAY(DATE('now', 'start of month', '-1 month')) 
                    - JULIANDAY(MIN(t.date_assigned))
                ) 
                - (
                    SELECT COUNT(*) 
                    FROM vacations 
                    WHERE user_id = t.user_id 
                    AND vacation_date BETWEEN MIN(t.date_assigned) 
                                        AND DATE('now', 'start of month', '-1 month')
                )
        END AS days_assigned
    FROM tasks t
    LEFT JOIN vacations v ON v.user_id = t.user_id
    WHERE t.user_id = ?
    GROUP BY t.task

    )


    SELECT 
        l.task,     
        printf("%.2f%%", COALESCE(current_month_completed_tasks.completed_tasks, 0) * 100.0 / COALESCE(current_month.days_assigned, 1)) AS current_month_percentage,
        printf("%.2f%%", COALESCE(previous_month_completed_tasks.completed_tasks, 0) * 100.0 / COALESCE(previous_month.days_assigned, 1)) AS previous_month_percentage,
        printf("%.2f%%", COALESCE(two_month_completed_tasks.completed_tasks, 0) * 100.0 / COALESCE(two_month.days_assigned, 1)) AS two_month_percentage,
        printf("%.2f%%", COALESCE(total_completed_tasks.completed_tasks, 0) * 100.0 / COALESCE(days_assigned.days_assigned, 1)) AS total_percentage,
        --COALESCE(total_completed_tasks.completed_tasks, 0) AS total_complete,
        --COALESCE(previous_month_completed_tasks.completed_tasks, 0) AS previous_month_complete,
        --COALESCE(current_month.days_assigned, 0) AS current_month_days_assigned,
        --COALESCE(previous_month.days_assigned, 0) AS previous_month_days_assigned,
        --COALESCE(two_month.days_assigned, 0) AS two_month_days_assigned,
        --COALESCE(previous_month_completed_tasks.completed_tasks, 0) AS previous_month_complete,
        --COALESCE(two_month_completed_tasks.completed_tasks, 0) AS two_month_complete,
        COALESCE(days_assigned.days_assigned, 0) AS total_days_assigned
        
    FROM 
        list l
        
    -- Completed tasks for two months back
    LEFT JOIN 
        (SELECT task, COUNT(*) AS completed_tasks 
        FROM tasks t
        LEFT JOIN vacations v 
        ON t.date_assigned = v.vacation_date AND v.user_id = t.user_id
        WHERE t.user_id = ? AND completion_status = true 
        AND v.vacation_date IS NULL -- Exclude tasks completed on vacation days
        AND date_assigned BETWEEN DATE('now', 'start of month', '-2 months') AND DATE('now', 'start of month', '-1 months','-1 day')
        GROUP BY task) AS two_month_completed_tasks
    ON 
        l.task = two_month_completed_tasks.task
        
    -- Completed tasks for previous month
    LEFT JOIN 
        (SELECT task, COUNT(*) AS completed_tasks 
        FROM tasks t
        LEFT JOIN vacations v 
        ON t.date_assigned = v.vacation_date AND v.user_id = t.user_id
        WHERE t.user_id = ? AND completion_status = true 
        AND v.vacation_date IS NULL -- Exclude tasks completed on vacation days
        AND date_assigned BETWEEN DATE('now', 'start of month', '-1 month') AND DATE('now', 'start of month', '-1 day')
        GROUP BY task) AS previous_month_completed_tasks
    ON 
        l.task = previous_month_completed_tasks.task
        
    -- Completed tasks for current month
    LEFT JOIN 
        (SELECT task, COUNT(*) AS completed_tasks
        FROM tasks t
        LEFT JOIN vacations v 
        ON t.date_assigned = v.vacation_date AND v.user_id = t.user_id
        WHERE t.user_id = ? AND t.completion_status = true 
        AND v.vacation_date IS NULL -- Exclude tasks completed on vacation days
        AND date_assigned BETWEEN DATE('now', 'start of month') AND DATE('now')
        GROUP BY t.task) AS current_month_completed_tasks
    ON 
        l.task = current_month_completed_tasks.task    
        
    -- Total completed tasks
    LEFT JOIN 
        (SELECT t.task, COUNT(*) AS completed_tasks 
        FROM tasks t
        LEFT JOIN vacations v 
        ON t.date_assigned = v.vacation_date AND v.user_id = t.user_id
        WHERE t.user_id = ? 
        AND t.completion_status = true 
        AND v.vacation_date IS NULL -- Exclude tasks completed on vacation days
        GROUP BY t.task) AS total_completed_tasks
    ON 
        l.task = total_completed_tasks.task
        
    -- Days assigned for current month
    LEFT JOIN current_month 
    ON l.task = current_month.task

    -- Days assigned for previous month
    LEFT JOIN previous_month 
    ON l.task = previous_month.task

    -- Days assigned for two month
    LEFT JOIN two_month 
    ON l.task = two_month.task

    -- Days assigned total
    LEFT JOIN
        (SELECT 
            t.task, 
            (JULIANDAY(DATE('now')) - JULIANDAY(MIN(t.date_assigned)) + 1) 
            - (
                SELECT COUNT(*) 
                FROM vacations v 
                WHERE v.user_id = t.user_id 
                AND v.vacation_date >= MIN(t.date_assigned) 
                AND v.vacation_date <= DATE('now')
            ) AS days_assigned
        FROM tasks t
        WHERE t.user_id = ?
        GROUP BY t.task) AS days_assigned
    ON l.task = days_assigned.task


    

    WHERE l.user_id = ?
    ORDER BY COALESCE(current_month_completed_tasks.completed_tasks, 0) * 100.0 / COALESCE(current_month.days_assigned, 1) DESC;
                            
        ''', (user_id,user_id,user_id,user_id,user_id,user_id,user_id,user_id,user_id,user_id))
    stats_list = [ {'task':row[0], 'current month':row[1],'previous month':row[2], 'two months':row[3], 'total percentage':row[4], 'days assigned count':int(row[5])} for row in main_table]
    rows = list(stats_list)

    return rows




if __name__ == '__main__':
    main_table = generate_main_table(3)
    print(main_table)
    print('done...')
    




