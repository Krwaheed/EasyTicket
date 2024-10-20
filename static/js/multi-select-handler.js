document.addEventListener('DOMContentLoaded', function () {
    const interestButtons = document.querySelectorAll('.interest-option');
    const form = document.querySelector('.signup-form');

  const subcategoryContainers = {
    '1': document.getElementById('subcategory-movies'),  // Movies
    '10': document.getElementById('subcategory-music'),  // Music
    '19': document.getElementById('subcategory-sports'), // Sports
    '28': document.getElementById('subcategory-theater'), // Theater
    '3': null,  // Comedy (no subcategories)
    '63': null, // Drama (no subcategories)

    // Subcategories for Movies
    '2': document.getElementById('subcategory-action'),
    '9': document.getElementById('subcategory-animated'),
    '4': document.getElementById('subcategory-romance'),
    '5': document.getElementById('subcategory-horror'),
    '6': document.getElementById('subcategory-thriller'),
    '7': document.getElementById('subcategory-sci-fi'),

    // Subcategories for Music
    '11': document.getElementById('subcategory-pop'),
    '12': document.getElementById('subcategory-rock'),
    '15': document.getElementById('subcategory-hip-hop'),
    '13': document.getElementById('subcategory-jazz'),
    '14': document.getElementById('subcategory-classical'),
    '16': document.getElementById('subcategory-country'),
    '17': document.getElementById('subcategory-electronic'),
    '18': document.getElementById('subcategory-reggae'),

    // Subcategories for Sports
    '21': document.getElementById('subcategory-basketball'),
    '20': document.getElementById('subcategory-football'),
    '23': document.getElementById('subcategory-soccer'),
    '22': document.getElementById('subcategory-tennis'),
    '24': document.getElementById('subcategory-cricket'),
    '25': document.getElementById('subcategory-hockey'),
    '26': document.getElementById('subcategory-swimming'),

    // Subcategories for Theater
    '29': document.getElementById('subcategory-musical'),
    '30': document.getElementById('subcategory-opera'),
    '32': document.getElementById('subcategory-play'),

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
