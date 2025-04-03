CREATE DATABASE IF NOT EXISTS mydb;

DROP mydb;

USE mydb;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);
DROP TABLE users;

SELECT username from users

USE mydb;

SELECT * FROM users
