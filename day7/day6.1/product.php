<?php
$host = 'localhost';
$username = 'root';
$password = '';
$database = 'product_database';


$conn = new mysqli($host, $username, $password, $database);


if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Fetch products from database
$sql = "SELECT * FROM products";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    $products = array();
    while ($row = $result->fetch_assoc()) {
        $products[] = array(
            'id' => $row['id'],
            'name' => $row['name'],
            'description' => $row['description'],
            'image_url' => $row['image_url']
        );
    }
    // Output products as JSON
    header('Content-Type: application/json');
    echo json_encode($products);
} else {
    echo "No products found";
}

// Close MySQL connection
$conn->close();

