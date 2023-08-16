CREATE TABLE tasks(
    id INTEGER primary key,
    user_id INTEGER,
    task_text TEXT NOT NULL,
    planned_date DATE,
    added_at TIMESTAMP default current_timestamp not null,
    finished_at TIMESTAMP default NULL
);
