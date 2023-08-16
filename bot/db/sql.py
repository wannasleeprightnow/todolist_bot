CHECK_TASK_COPY = """SELECT task_text
FROM tasks
WHERE task_text = ? AND planned_date = ? AND user_id = ? 
"""

ADD_TASK = """INSERT INTO tasks
(user_id, task_text, planned_date, added_at)
VALUES(?, ?, ?, current_timestamp)
"""

DAYS_TASKS = """SELECT task_text, finished_at
FROM tasks
WHERE user_id = ? AND planned_date LIKE ?
"""

DELETE_TASK = """DELETE 
FROM tasks
WHERE user_id = ? AND task_text = ?
"""

FINISH_TASK = """UPDATE tasks
SET finished_at = current_timestamp
WHERE user_id = ? AND task_text = ?
"""
