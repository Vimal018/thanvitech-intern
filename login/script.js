$(document).ready(function() {
    // Check username availability on keyup event
    $('#register_username').keyup(function() {
        var username = $(this).val();

        $.ajax({
            type: 'POST',
            url: 'check_username.php',
            data: { username: username },
            success: function(response) {
                if (response == 'taken') {
                    $('#username_status').html('<span style="color: red;">Username taken!</span>');
                    $('#registerForm').attr('data-username-valid', 'false');
                } else {
                    $('#username_status').html('<span style="color: green;">Username available</span>');
                    $('#registerForm').attr('data-username-valid', 'true');
                }
            }
        });
    });

    // Handle registration form submission
    $('#registerForm').submit(function(event) {
        event.preventDefault(); // Prevent the form from submitting normally

        // Check if username availability is validated
        if ($(this).attr('data-username-valid') !== 'true') {
            alert('Please choose a different username.');
            return;
        }

        var username = $('#register_username').val();
        var password = $('#register_password').val();

        $.ajax({
            type: 'POST',
            url: 'register.php',
            data: {
                username: username,
                password: password
            },
            success: function(response) {
                if (response == 'success') {
                    alert('Registration successful!');
                    // Optionally, redirect to login page
                    // window.location.href = 'index.html';
                } else {
                    alert('Registration failed. Please try again.');
                }
            }
        });
    });

    // Handle login form submission
    $('#loginForm').submit(function(event) {
        event.preventDefault(); // Prevent the form from submitting normally

        var username = $('#login_username').val();
        var password = $('#login_password').val();

        $.ajax({
            type: 'POST',
            url: 'login.php',
            data: {
                username: username,
                password: password
            },
            success: function(response) {
                if (response == 'success') {
                    alert('Login successful!');
                    // Redirect to welcome page or dashboard
                    // window.location.href = 'welcome.php';
                } else {
                    alert('Invalid username or password.');
                }
            }
        });
    });
});
