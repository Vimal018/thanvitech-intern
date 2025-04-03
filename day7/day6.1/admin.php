<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Admin Dashboard</title>
  <link rel="stylesheet" href= "styles1.css" />
</head>
<body>
  <div class="admin-dashboard">
    <h1>Admin Dashboard</h1>

    <!-- Form to create a new product -->
    <h2>Create Product</h2>
    <form id="create-product-form" action="create_product.php" method="post">
      <label for="product_name">Product Name:</label><br>
      <input type="text" id="product_name" name="product_name" required><br><br>
      <label for="product_description">Description:</label><br>
      <textarea id="product_description" name="product_description" required></textarea><br><br>
      <label for="product_image_url">Image URL:</label><br>
      <input type="text" id="product_image_url" name="product_image_url" required><br><br>
      <button type="submit">Create Product</button>
    </form>

    <!-- List of existing products in table format -->
    <h2>Products</h2>
    <table id="product-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Description</th>
          <th>Image</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody id="product-list">
        <!-- Product rows will be inserted dynamically here -->
      </tbody>
    </table>
  </div>

  <script>
    // Fetch products from backend and display them in the table
    function fetchProducts() {
      fetch('fetch_products.php')
        .then(response => response.json())
        .then(products => {
          const productList = document.getElementById('product-list');
          productList.innerHTML = '';

          products.forEach(product => {
            const row = `
              <tr>
                <td>${product.id}</td>
                <td>${product.name}</td>
                <td>${product.description}</td>
                <td><img src="${product.image_url}" alt="${product.name}" width="200" height="200"></td>
                <td>
                  <button class="edit-button" onclick="editProduct(${product.id})">Edit</button>
          <button class="delete-button" onclick="deleteProduct(${product.id})">Delete</button>
                </td>
              </tr>
            `;
            productList.innerHTML += row;
          });
        })
        .catch(error => console.error('Error fetching products:', error));
    }

    // Function to edit a product
    function editProduct(productId) {
  // Fetch existing product details to get current values
  fetch(`fetch_products.php?product_id=${productId}`)
    .then(response => response.json())
    .then(product => {
      // Ask user which fields they want to update
      const updateChoice = prompt('What do you want to update? Enter "name", "description", "image", or leave empty to keep existing values:');
      
      // Prompt for new values based on user choice
      let newName = product.name;
      let newDescription = product.description;
      let newImage = product.image_url;

      if (updateChoice === 'name') {
        newName = prompt('Enter new product name:');
      } else if (updateChoice === 'description') {
        newDescription = prompt('Enter the product description:');
      } else if (updateChoice === 'image') {
        newImage = prompt('Enter the Image URL:');
      } else {
        // User chose not to update anything
        alert('No fields updated.');
        return;
      }

      // Prepare FormData with updated or existing values
      const formData = new FormData();
      formData.append('product_id', productId);
      formData.append('product_name', newName);
      formData.append('product_description', newDescription);
      formData.append('product_image_url', newImage);

      // Perform the fetch request to update the product
      fetch('edit_product.php', {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(result => {
        if (result.success) {
          alert('Product updated successfully!');
          fetchProducts(); // Refresh product list
        } else {
          alert('Error updating product: ' + result.error);
        }
      })
      .catch(error => console.error('Error updating product:', error));
    })
    .catch(error => console.error('Error fetching product details:', error));
}


    

    // Function to delete a product
    function deleteProduct(productId) {
      if (confirm('Are you sure you want to delete this product?')) {
        const formData = new FormData();
        formData.append('product_id', productId);

        fetch('delete_product.php', {
          method: 'POST',
          body: formData
        })
        .then(response => response.text())
        .then(result => {
          alert('Product deleted successfully!');
          fetchProducts(); // Refresh product list
        })
        .catch(error => console.error('Error deleting product:', error));
      }
    }

    // Fetch products when page loads
    fetchProducts();
  </script>
</body>
</html>
