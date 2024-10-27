console.log("User Dashboard loaded successfully.");

// JavaScript for tab functionality
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;

    // Hide all tabcontent
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Remove the 'active' class from all tablinks
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab and add 'active' class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";

    // Store the active tab in localStorage
    localStorage.setItem("activeTab", tabName);
}

// Function to open the default or saved tab on page load
function openDefaultTab() {
    var activeTab = localStorage.getItem("activeTab");
    if (activeTab) {
        document.getElementById(activeTab).style.display = 'block';
        document.querySelector(`button[onclick="openTab(event, '${activeTab}')"]`).classList.add('active');
    } else {
        // Open default tab
        document.getElementById("defaultOpen").click();
    }
}

// Call this function to open the saved tab (or default) on page load
openDefaultTab();

// JavaScript for sorting functionality
document.getElementById('sort_by').addEventListener('change', function() {
    let sortBy = this.value;
    let eventsGrid = document.getElementById('events-grid');
    let eventCards = Array.from(eventsGrid.getElementsByClassName('event-card'));

    eventCards.sort(function(a, b) {
        let aValue, bValue;
        if (sortBy === 'start_time') {
            aValue = new Date(a.getAttribute('data-start-time'));
            bValue = new Date(b.getAttribute('data-start-time'));
        } else if (sortBy === 'venue') {
            aValue = a.getAttribute('data-venue').toLowerCase();
            bValue = b.getAttribute('data-venue').toLowerCase();
        } else if (sortBy === 'event_name') {
            aValue = a.getAttribute('data-name').toLowerCase();
            bValue = b.getAttribute('data-name').toLowerCase();
        }
        return aValue < bValue ? -1 : aValue > bValue ? 1 : 0;
    });

    eventCards.forEach(function(card) {
        eventsGrid.appendChild(card);
    });
});

// Function to check if an event's date has passed
function checkEventDates() {
    const eventCards = document.querySelectorAll('.event-card');
    const currentDate = new Date();

    eventCards.forEach(card => {
        const eventDate = new Date(card.getAttribute('data-event-date'));

        // If the event date is in the past, show the warning message
        if (eventDate < currentDate) {
            const unavailableMessage = card.querySelector('.event-unavailable');
            unavailableMessage.style.display = 'block'; // Show the message
        }
    });
}

// Call the function to check for past events when the page loads
checkEventDates();
