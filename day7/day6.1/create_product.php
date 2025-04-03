<?php
session_start();
include_once 'db.php'; // Include database connection

if ($_SERVER["REQUEST_METHOD"] == "POST") {
  $product_name = $_POST['product_name'];
  $product_description = $_POST['product_description'];
  $product_image_url = $_POST['product_image_url'];

  // Example: Insert product into the database
  $sql = "INSERT INTO products (name, description, image_url) VALUES (?, ?, ?)";
  $stmt = $conn->prepare($sql);
  $stmt->bind_param("sss", $product_name, $product_description, $product_image_url);

  if ($stmt->execute()) {
    header("Location: admin.php"); // Redirect to admin dashboard
    exit();
  } else {
    echo "Error: " . $sql . "<br>" . $conn->error;
  }

  $stmt->close();
  $conn->close();
}
