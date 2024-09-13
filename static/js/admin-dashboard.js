document.addEventListener('DOMContentLoaded', () => {
    // Fetches the admin session details from the backend
    fetch('/api/admin/session')
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
    fetch('/api/users')
        .then(response => response.json())
        .then(users => {
            const userList = document.getElementById('user-list');
            userList.innerHTML = ''; // Clear existing entries
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
    fetch('/api/events')
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

// Commented out functions related to features not yet implemented in the backend
/*
function viewSavedEvents(userId) {
    // Placeholder for future implementation
}

function viewPastPurchases(userId) {
    // Placeholder for future implementation
}

function blockEvent(eventId) {
    // Placeholder for future implementation
}
*/

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

