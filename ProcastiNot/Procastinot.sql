-- Active: 1706013118089@@127.0.0.1@3306
USE todo;
CREATE TABLE tasks (
	id INT AUTO_INCREMENT PRIMARY KEY,
    task_name VARCHAR(250) NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT 0 );
    
INSERT INTO tasks (task_name, description) VALUES
('Buy groceries', 'Milk, eggs, bread'),
('Complete SQL Project', 'Make TO-DO Application');

