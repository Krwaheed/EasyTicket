document.addEventListener('DOMContentLoaded', () => {
    // Fetches the admin session details from the backend
    fetch('/api/admin/session')  // Adjust this later to backend API route to database 
        .then(response => response.json())
        .then(data => {
            if (data.username) {
                document.getElementById('admin-username').textContent = data.username;
                loadUsers();
                loadEvents();
            } else {
                window.location.href = 'admin-login.html';
            }
        })
        .catch(error => {
            console.error('Error fetching admin session:', error);
            window.location.href = 'admin-login.html';
        });

    // Set up modals
    setupModals();
});

// Function to load users dynamically
function loadUsers() {
    fetch('/api/users')  // Adjust this later to backend API route for fetching users from database
        .then(response => response.json())
        .then(users => {
            const userList = document.getElementById('user-list');
            userList.innerHTML = '';

            users.forEach(user => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${user.username}</td>
                    <td>${user.email}</td>
                    <td><button onclick="viewSavedEvents('${user.id}')">View Saved Events</button></td>
                    <td><button onclick="viewPastPurchases('${user.id}')">View Past Purchases</button></td>
                    <td><button class="delete-btn" onclick="deleteUser('${user.id}')">Delete Account</button></td>
                `;
                userList.appendChild(row);
            });
        })
        .catch(error => console.error('Error loading users:', error));
}

// Function to load events dynamically
function loadEvents() {
    fetch('/api/events')  // Adjust this later to backend API route for fetching events (rapidAPI)
        .then(response => response.json())
        .then(events => {
            const eventList = document.getElementById('event-list');
            eventList.innerHTML = '';

            events.forEach(event => {
                const listItem = document.createElement('li');
                listItem.innerHTML = `
                    Event Name: ${event.name} - 
                    <button class="block-btn" onclick="blockEvent('${event.id}')">Block Event</button>
                `;
                eventList.appendChild(listItem);
            });
        })
        .catch(error => console.error('Error loading events:', error));
}

// Function to delete a user
function deleteUser(userId) {
    if (confirm('Are you sure you want to delete this user?')) {
        fetch(`/api/users/${userId}`, { method: 'DELETE' })
            .then(response => {
                if (response.ok) {
                    alert('User deleted successfully.');
                    loadUsers();
                } else {
                    alert('Failed to delete user.');
                }
            })
            .catch(error => console.error('Error deleting user:', error));
    }
}

// Function to block an event
function blockEvent(eventId) {
    if (confirm('Are you sure you want to block this event?')) {
        fetch(`/api/events/${eventId}/block`, { method: 'POST' })
            .then(response => {
                if (response.ok) {
                    alert('Event blocked successfully.');
                    loadEvents();
                } else {
                    alert('Failed to block event.');
                }
            })
            .catch(error => console.error('Error blocking event:', error));
    }
}

// Function to view saved events (opens modal)
function viewSavedEvents(userId) {
    fetch(`/api/users/${userId}/saved-events`)  // Adjust this later for API route for fetching user saved events from database
        .then(response => response.json())
        .then(events => {
            const savedEventsList = document.getElementById('saved-events-list');
            savedEventsList.innerHTML = '';  // Clear previous list

            events.forEach(event => {
                const listItem = document.createElement('li');
                listItem.textContent = event.name;
                savedEventsList.appendChild(listItem);
            });

            document.getElementById('saved-events-modal').style.display = 'block';
        })
        .catch(error => console.error('Error loading saved events:', error));
}

// Function to view past purchases (opens modal)
function viewPastPurchases(userId) {
    fetch(`/api/users/${userId}/past-purchases`)  // Adjust this later for API route for fetching user past purchases from database
        .then(response => response.json())
        .then(purchases => {
            const pastPurchasesList = document.getElementById('past-purchases-list');
            pastPurchasesList.innerHTML = '';  // Clear previous list

            purchases.forEach(purchase => {
                const listItem = document.createElement('li');
                listItem.textContent = `Event: ${purchase.eventName}, Date: ${purchase.date}`;
                pastPurchasesList.appendChild(listItem);
            });

            document.getElementById('past-purchases-modal').style.display = 'block';
        })
        .catch(error => console.error('Error loading past purchases:', error));
}

// Function to handle modals (open/close)
function setupModals() {
    const savedEventsModal = document.getElementById('saved-events-modal');
    const pastPurchasesModal = document.getElementById('past-purchases-modal');

    // Close modal for saved events
    document.getElementById('close-saved-events').onclick = function() {
        savedEventsModal.style.display = 'none';
    };

    // Close modal for past purchases
    document.getElementById('close-past-purchases').onclick = function() {
        pastPurchasesModal.style.display = 'none';
    };

    // Close modals when clicking outside of them
    window.onclick = function(event) {
        if (event.target == savedEventsModal) {
            savedEventsModal.style.display = 'none';
        }
        if (event.target == pastPurchasesModal) {
            pastPurchasesModal.style.display = 'none';
        }
    };
}

