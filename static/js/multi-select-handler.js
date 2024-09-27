document.addEventListener('DOMContentLoaded', function () {
    const interestButtons = document.querySelectorAll('.interest-option');
    const form = document.querySelector('.signup-form');

    const subcategoryContainers = {
    '1': document.getElementById('subcategory-movies'), // Movies
    '10': document.getElementById('subcategory-music'), // Music
    '19': document.getElementById('subcategory-sports'), // Sports
    '28': document.getElementById('subcategory-theater'), // Theater
    '3': null, // Comedy (no subcategories)
    '63': null // Drama (no subcategories)
};


    // Handle the main interest buttons
    interestButtons.forEach(button => {
        button.addEventListener('click', function () {
            const interest = this.getAttribute('data-value');

            // Toggle selected state for main categories
            this.classList.toggle('selected');

            // Show/hide subcategories if they exist
            if (subcategoryContainers[interest]) {
                const subcategoryDiv = subcategoryContainers[interest];
                if (subcategoryDiv.style.display === 'none' || subcategoryDiv.style.display === '') {
                    subcategoryDiv.style.display = 'block';  // Show subcategories
                } else {
                    subcategoryDiv.style.display = 'none';   // Hide subcategories
                }
            }
        });
    });

    // Handle the subcategory buttons
    const subcategoryButtons = document.querySelectorAll('.subcategory-option');
    subcategoryButtons.forEach(button => {
        button.addEventListener('click', function () {
            this.classList.toggle('selected');  // Toggle the highlight for subcategories
        });
    });

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        // Collect selected main interests
        const selectedInterests = Array.from(interestButtons)
            .filter(button => button.classList.contains('selected'))
            .map(button => button.getAttribute('data-value'));

        // Collect selected subcategories
        const selectedSubcategories = Array.from(document.querySelectorAll('.subcategory-option'))
            .filter(button => button.classList.contains('selected'))
            .map(button => button.getAttribute('data-value'));

        const formData = new FormData(form);
        selectedInterests.forEach(interest => formData.append('interests', interest));
        selectedSubcategories.forEach(subcategory => formData.append('subcategories', subcategory));

        // Submit form with selected interests and subcategories
        fetch(form.action, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.href = data.redirect_url;
            } else {
                console.error('Error:', data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
