<?php
include_once 'db.php'; // Include database connection

if ($_SERVER["REQUEST_METHOD"] == "POST") {
  $product_id = $_POST['product_id'];
  $product_name = $_POST['product_name'];
  $product_description = $_POST['product_description'];
  $product_image_url = $_POST['product_image_url'];

  // Update product in the database
  $sql = "UPDATE products SET name=?, description=?, image_url=? WHERE id=?";
  $stmt = $conn->prepare($sql);
  $stmt->bind_param("sssi", $product_name, $product_description, $product_image_url, $product_id);

  if ($stmt->execute()) {
    // Product update successful
    header("Location: admin.php"); // Redirect to admin dashboard
    exit();
  } else {
    // Product update failed
    echo "Error updating product: " . $conn->error;
  }

  $stmt->close();
  $conn->close();
}
