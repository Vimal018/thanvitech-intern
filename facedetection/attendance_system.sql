-- Active: 1718720962027@@127.0.0.1@3306@attendance_system
CREATE DATABASE IF NOT EXISTS attendance_system;
USE attendance_system;


DROP TABLE teacher;


CREATE TABLE teacher (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    face_image LONGBLOB
);



SELECT * FROM teacher;



-- 1. Create the database
CREATE DATABASE IF NOT EXISTS attendance_system;

-- Use the created database
USE attendance_system;

-- 2. Create the 'teacher' table
CREATE TABLE IF NOT EXISTS teacher (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    face_image LONGBLOB,
    password VARCHAR(255) NOT NULL,  
    UNIQUE (id)  -- Ensure unique IDs
);

-- 3. Create the 'attendance' table
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES teacher(id)  -- Ensure user_id exists in teacher table
);

DROP Table attendance;

ALTER TABLE teacher
ADD COLUMN password VARCHAR(255) NOT NULL;

CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_id INT NOT NULL,
    teacher_name VARCHAR(255) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES teacher(id)
);

ALTER TABLE attendance ADD COLUMN date DATE;

USE mysql;
UPDATE user SET authentication_string=PASSWORD('new_password') WHERE User='root';
FLUSH PRIVILEGES;
SELECT user, host FROM mysql.user WHERE user = 'root';

