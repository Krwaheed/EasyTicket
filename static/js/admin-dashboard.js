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
                    <td><button onclick="viewSavedEvents('${user.user_id}')">View Saved </button></td>
                    <td><button onclick="viewUserInterests('${user.user_id}')">View Interests </button></td>
                    <td><button class="delete-btn" onclick="deleteUser('${user.user_id}')">Delete</button></td>
                `;
                userList.appendChild(row);
            });
        })
        .catch(error => console.error('Error loading users:', error));
}

function viewUserInterests(userId) {
    fetch(`/admin/view-user-interests/${userId}`)
        .then(response => response.json())
        .then(data => {
            const interestsList = document.getElementById('user-interests-list');
            interestsList.innerHTML = '';

            if (data.interests.length > 0) {
                data.interests.forEach(interest => {
                    const listItem = document.createElement('li');
                    listItem.textContent = interest.interest_name;
                    interestsList.appendChild(listItem);
                });
            } else {
                interestsList.innerHTML = '<li>No interests for this user.</li>';
            }

            const userInterestsModal = document.getElementById('user-interests-modal');
            userInterestsModal.style.display = 'block';
        })
        .catch(error => console.error('Error fetching user interests:', error));
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
                    loadUsers(); // Ensure this function is defined to reload the user list
                } else {
                    alert('Failed to delete user: ' + response.statusText);
                }
            })
            .catch(error => console.error('Error deleting user:', error));
    }
}

function viewSavedEvents(userId) {
    fetch(`/admin/view-saved-events/${userId}`)
        .then(response => response.json())
        .then(data => {
            const savedEventsList = document.getElementById('saved-events-list');
            savedEventsList.innerHTML = ''; // Clear the previous content

            if (data.events.length > 0) {
                data.events.forEach(event => {
                    const listItem = document.createElement('li');
                    listItem.innerHTML = `
                        <h4>${event.event_name}</h4>
                        <p>Date: ${event.event_date}</p>
                        <p>Location: ${event.location}</p>
                    `;
                    savedEventsList.appendChild(listItem);
                });
            } else {
                savedEventsList.innerHTML = '<li>No saved events for this user.</li>';
            }

            // Show the modal
            const savedEventsModal = document.getElementById('saved-events-modal');
            savedEventsModal.style.display = 'block';
        })
        .catch(error => console.error('Error fetching saved events:', error));
}

// Function to handle modals (open/close)
function setupModals() {
    const savedEventsModal = document.getElementById('saved-events-modal');
    const userInterestsModal = document.getElementById('user-interests-modal');

    // Close modal for saved events
    document.getElementById('close-saved-events').onclick = function() {
        savedEventsModal.style.display = 'none';
    };
    document.getElementById('close-user-interests').onclick = function() {
        userInterestsModal.style.display = 'none';
    };

    // Close modals when clicking outside of them
    window.onclick = function(event) {
        if (event.target == savedEventsModal) {
            savedEventsModal.style.display = 'none';
        }
        if (event.target == userInterestsModal) {
            userInterestsModal.style.display = 'none';
        }
    };
}

