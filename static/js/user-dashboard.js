// Placeholder JavaScript file
console.log("User Dashboard loaded successfully.");

    // JavaScript for frontend sorting
    document.getElementById('sort_by').addEventListener('change', function() {
    let sortBy = this.value;  // Get the selected sorting option
    let eventsGrid = document.getElementById('events-grid');  // Get the events grid
    let eventCards = Array.from(eventsGrid.getElementsByClassName('event-card'));  // Convert HTMLCollection to array

    // Sort the event cards based on the selected criteria
    eventCards.sort(function(a, b) {
    let aValue, bValue;

    if (sortBy === 'start_time') {
    // Sort by start_time
    aValue = new Date(a.getAttribute('data-start-time'));
    bValue = new Date(b.getAttribute('data-start-time'));
} else if (sortBy === 'venue') {
    // Sort by venue name (case-insensitive)
    aValue = a.getAttribute('data-venue').toLowerCase();
    bValue = b.getAttribute('data-venue').toLowerCase();
} else if (sortBy === 'event_name') {
    // Sort by event name (case-insensitive)
    aValue = a.getAttribute('data-name').toLowerCase();
    bValue = b.getAttribute('data-name').toLowerCase();
}

    if (aValue < bValue) return -1;
    if (aValue > bValue) return 1;
    return 0;
});

    // Reorder the event cards in the DOM
    eventCards.forEach(function(card) {
    eventsGrid.appendChild(card);  // This moves each card in sorted order
});
});

