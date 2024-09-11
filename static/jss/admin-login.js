// JavaScript to handle form submission and send credentials to the backend
document.getElementById('admin-login-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent default form submission

    // Get the input values
    const username = document.getElementById('admin-username').value;
    const password = document.getElementById('admin-password').value;

    // Send the login data to the backend for validation
    fetch('/api/admin-login', {  // Adjust this later to actual route backend setup
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => {
        if (response.ok) {
            // If the backend returns success, redirect to the admin dashboard
            window.location.href = 'admin-dashboard.html';
        } else {
            // Handle login failure (e.g., invalid credentials)
            alert('Login failed. Please check your credentials and try again.');
        }
    })
    .catch(error => console.error('Error during login:', error));
});