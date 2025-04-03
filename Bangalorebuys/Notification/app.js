const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

// Parse application/json requests
app.use(bodyParser.json());

// Handle POST request to send notification
app.post('/send-notification', (req, res) => {
    const { name, email, message } = req.body;
    
    // Here you can implement logic to send notification to the seller
    // For example, send an email to the seller with the details
    
    // Simulating a response
    res.json({ message: 'Notification sent successfully' });
});

app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
