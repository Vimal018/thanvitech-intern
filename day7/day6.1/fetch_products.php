<?php
include_once 'db.php'; // Include database connection

$sql = "SELECT * FROM products";
$result = $conn->query($sql);

$products = array();

if ($result->num_rows > 0) {
  while ($row = $result->fetch_assoc()) {
    $products[] = array(
      'id' => $row['id'],
      'name' => $row['name'],
      'description' => $row['description'],
      'image_url' => $row['image_url']
    );
  }
}

echo json_encode($products);
$conn->close();
