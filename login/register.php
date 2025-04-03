<?php
// Database connection parameters
$host = 'localhost';
$username = 'root';
$password = '';
$database = 'mydb';

// Establish MySQL database connection
$mysqli = new mysqli($host, $username, $password, $database);

// Check connection
if ($mysqli->connect_error) {
    die("Connection failed: " . $mysqli->connect_error);
}

// Retrieve username and password from POST data
$username = $_POST['username'];
$password = $_POST['password'];

// Hash the password (for security)
$hashed_password = password_hash($password, PASSWORD_DEFAULT);

// Insert user into database
$query = "INSERT INTO users (username, password) VALUES ('$username', '$hashed_password')";
if ($mysqli->query($query) === TRUE) {
    echo 'success';
} else {
    echo 'error';
}

// Close database connection
$mysqli->close();
