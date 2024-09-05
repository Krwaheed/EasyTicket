document.addEventListener('DOMContentLoaded', function () {
    const interestButtons = document.querySelectorAll('.interest-option');
    const form = document.querySelector('.signup-form');

    interestButtons.forEach(button => {
        button.addEventListener('click', function () {
            this.classList.toggle('selected');  // Toggle the 'selected' class on click
        });
    });

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        
        const selectedInterests = Array.from(interestButtons)
            .filter(button => button.classList.contains('selected'))
            .map(button => button.getAttribute('data-value'));

        const formData = new FormData(form);
        selectedInterests.forEach(interest => formData.append('interests', interest));

        // Optionally log to console or inspect the FormData contents
        console.log("Selected interests:", selectedInterests);

        // Submit form data via fetch API to the server
        fetch(form.action, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => console.log('Success:', data))
        .catch(error => console.error('Error:', error));
    });
});