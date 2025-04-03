document.getElementById("notificationForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form from submitting normally
    
    // Get form data
    const name = document.getElementById("customerName").value;
    const email = document.getElementById("customerEmail").value;
    const message = document.getElementById("message").value;
    
    // Create data object to send via AJAX
    const data = {
        name: name,
        email: email,
        message: message
    };
    
    // Send AJAX request
    fetch('/send-notification', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        alert('Notification sent successfully'); // Show success message to user
        // Optionally, clear the form fields
        document.getElementById("notificationForm").reset();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to send notification');
    });
});
