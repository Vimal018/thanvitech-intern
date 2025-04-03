-- Active: 1718720962027@@127.0.0.1@3306


CREATE DATABASE my_new_database;

USE my_new_database;



CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

SHOW DATABASES;

USE my_new_database;


SELECT username FROM users 

SELECT PASSWORD FROM users

SELECT * FROM users
