<?php
include_once 'db.php'; // Include database connection

if ($_SERVER["REQUEST_METHOD"] == "POST") {
  $product_id = $_POST['product_id'];

  // Delete product from the database
  $sql = "DELETE FROM products WHERE id=?";
  $stmt = $conn->prepare($sql);
  $stmt->bind_param("i", $product_id);

  if ($stmt->execute()) {
    // Product deletion successful
    header("Location: admin.php"); // Redirect to admin dashboard
    exit();
  } else {
    // Product deletion failed
    echo "Error deleting product: " . $conn->error;
  }

  $stmt->close();
  $conn->close();
}
