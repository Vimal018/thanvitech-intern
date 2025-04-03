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

// Retrieve username from POST data
$username = $_POST['username'];

// Query to check if username exists
$query = "SELECT * FROM users WHERE username='$username'";
$result = $mysqli->query($query);

if ($result->num_rows > 0) {
    // Username taken
    echo 'taken';
} else {
    // Username available
    echo 'available';
}

// Close database connection
$mysqli->close();
