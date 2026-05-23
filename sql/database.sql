-- ==========================================
-- Student Task Manager Database Schema
-- Designed for beginners learning MySQL & Flask
-- Database Engine: InnoDB
-- ==========================================

-- 1. DATABASE CREATION
-- We create the database if it doesn't already exist and switch to using it.
CREATE DATABASE IF NOT EXISTS student_task_manager;
USE student_task_manager;

-- ==========================================
-- TABLE 1: students
-- Stores primary information of students enrolled.
-- ==========================================
DROP TABLE IF EXISTS students;
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(10) NULL,
    date_of_birth DATE NULL,
    mobile_number VARCHAR(15) NULL,
    email VARCHAR(100) UNIQUE NULL,
    course_name VARCHAR(100) NULL,
    admission_date DATE NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ==========================================
-- TABLE 2: attendance
-- Records daily attendance status of students.
-- ==========================================
DROP TABLE IF EXISTS attendance;
CREATE TABLE attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    attendance_date DATE NOT NULL,
    -- Status can be: 'Present', 'Absent', or 'Leave'
    attendance_status VARCHAR(10) NOT NULL,
    remarks VARCHAR(255) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key to ensure attendance belongs to an existing student
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ==========================================
-- TABLE 3: tasks
-- Stores information about academic tasks or assignments.
-- ==========================================
DROP TABLE IF EXISTS tasks;
CREATE TABLE tasks (
    task_id INT AUTO_INCREMENT PRIMARY KEY,
    task_title VARCHAR(100) NOT NULL,
    task_description TEXT NULL,
    due_date DATE NULL,
    maximum_marks INT NOT NULL DEFAULT 100,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ==========================================
-- TABLE 4: student_tasks
-- Represents the relationship between students and tasks.
-- Tracks student submissions, marks obtained, and remarks.
-- ==========================================
DROP TABLE IF EXISTS student_tasks;
CREATE TABLE student_tasks (
    student_task_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    task_id INT NOT NULL,
    -- Status can be: 'Pending', 'Submitted', or 'Graded'
    submission_status VARCHAR(20) DEFAULT 'Pending',
    marks_obtained DECIMAL(5,2) NULL,
    submission_date DATETIME NULL,
    remarks VARCHAR(255) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign keys to ensure valid references to students and tasks
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ==========================================
-- DATABASE INDEXES
-- Indexes improve search and retrieval performance on key columns.
-- ==========================================

-- Index on student_id in attendance table
CREATE INDEX idx_attendance_student ON attendance(student_id);

-- Index on attendance_date in attendance table
CREATE INDEX idx_attendance_date ON attendance(attendance_date);

-- Index on student_id in student_tasks table
CREATE INDEX idx_student_tasks_student ON student_tasks(student_id);

-- Index on task_id in student_tasks table
CREATE INDEX idx_student_tasks_task ON student_tasks(task_id);


-- ==========================================
-- SAMPLE DATA INSERTIONS
-- ==========================================

-- Insert 5 sample records into the students table
INSERT INTO students (first_name, last_name, gender, date_of_birth, mobile_number, email, course_name, admission_date) VALUES
('John', 'Doe', 'Male', '2005-04-12', '1234567890', 'john.doe@example.com', 'Computer Science', '2025-09-01'),
('Jane', 'Smith', 'Female', '2004-11-23', '0987654321', 'jane.smith@example.com', 'Information Technology', '2025-09-01'),
('Michael', 'Johnson', 'Male', '2005-07-19', '5551234567', 'michael.j@example.com', 'Software Engineering', '2025-09-05'),
('Emily', 'Davis', 'Female', '2006-01-30', '4449876543', 'emily.davis@example.com', 'Computer Science', '2025-09-01'),
('David', 'Wilson', 'Male', '2004-05-15', '3335557777', 'david.wilson@example.com', 'Data Science', '2025-09-10');

-- Insert 5 sample records into the tasks table
INSERT INTO tasks (task_title, task_description, due_date, maximum_marks) VALUES
('HTML & CSS Personal Website', 'Create a responsive personal portfolio website using basic HTML structures and vanilla CSS styling.', '2026-06-05', 100),
('Flask CRUD Application', 'Develop a beginner-friendly Student Task Manager web application using Flask, MySQL, and HTML templates.', '2026-06-15', 100),
('SQL Join Queries Practice', 'Complete the worksheet containing complex JOIN queries, subqueries, and grouping commands.', '2026-06-20', 50),
('Python Control Flow Exercises', 'Write Python scripts solving various algorithmic problems using loops, conditional statements, and functions.', '2026-05-30', 40),
('Database Normalization Report', 'Write a short report explaining 1NF, 2NF, and 3NF database normalization techniques with examples.', '2026-06-10', 80);
