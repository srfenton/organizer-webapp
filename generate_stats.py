
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

    