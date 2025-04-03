<?php
// Database connection parameters
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "base";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Fetch slides from database
$sql = "SELECT * FROM slides ORDER BY order_index";
$result = $conn->query($sql);

// Prepare data to send back as JSON
$slides = [];
if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $slides[] = $row;
    }
}

// Output JSON formatted data
header('Content-Type: application/json');
echo json_encode($slides);

// Close connection
$conn->close();

