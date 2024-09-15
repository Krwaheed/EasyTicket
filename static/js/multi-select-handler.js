document.addEventListener('DOMContentLoaded', function () {
    const interestButtons = document.querySelectorAll('.interest-option');
    const form = document.querySelector('.signup-form');

    interestButtons.forEach(button => {
        button.addEventListener('click', function () {
            this.classList.toggle('selected');
        });
    });

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const selectedInterests = Array.from(interestButtons)
            .filter(button => button.classList.contains('selected'))
            .map(button => button.getAttribute('data-value'));

        const formData = new FormData(form);
        selectedInterests.forEach(interest => formData.append('interests', interest));


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
