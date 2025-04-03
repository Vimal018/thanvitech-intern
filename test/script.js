
$(document).ready(function() {
    $('#registerForm').submit(function(e) {
        e.preventDefault();
        var username = $('#registerUsername').val();
        var password = $('#registerPassword').val();

        $.ajax({
            type: 'POST',
            url: 'register.php',
            data: { username: username, password: password },
            dataType: 'json',
            success: function(response) {
                if (response.success) {
                    $('#message').text('Registration successful').css('color', 'green');
                    $('#registerForm')[0].reset();  // Clear form inputs
                } else {
                    $('#message').text(response.message).css('color', 'red');
                }
            },
            error: function() {
                $('#message').text('Error: Unable to communicate with server').css('color', 'red');
            }
        });
    });

    $('#loginForm').submit(function(e) {
        e.preventDefault();
        var username = $('#loginUsername').val();
        var password = $('#loginPassword').val();

        $.ajax({
            type: 'POST',
            url: 'login.php',
            data: { username: username, password: password },
            dataType: 'json',
            success: function(response) {
                if (response.success) {
                    $('#message').text('Login successful').css('color', 'green');
                    // Redirect to dashboard or desired page after successful login
                    window.location.href = 'index.html';
                } else {
                    $('#message').text(response.message).css('color', 'red');
                }
            },
            error: function() {
                $('#message').text('Error: Unable to communicate with server').css('color', 'red');
            }
        });
    });
});
