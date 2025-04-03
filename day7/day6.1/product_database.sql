-- Active: 1718720962027@@127.0.0.1@3306@product_database


CREATE DATABASE product_database;

USE product_database;

DROP TABLE products;


CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    image_url VARCHAR(255) NOT NULL
);


INSERT INTO products (name, description, image_url) 
VALUES 
    ('Fig 1', 'Fig 1 Description', 'fig1.jpg'),
    ('Fig 2', 'Fig 2 Description', 'fig2.jpg'),
    ('Fig 3', 'Fig 3 Description', 'fig3.jpg'),
    ('Fig 4', 'Fig 4 Description', 'fig1.jpg'),
    ('Fig 5', 'Fig 5 Description', 'fig2.jpg'),
    ('Fig 6', 'Fig 6 Description', 'fig3.jpg'),
    ('Fig 7', 'Fig 7 Description', 'fig1.jpg'),
    ('Fig 8', 'Fig 8 Description', 'fig2.jpg'),
    ('Fig 9', 'Fig 9 Description', 'fig3.jpg');


SELECT * FROM products