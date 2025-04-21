document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('file');
    const questionInput = document.getElementById('question');
    const submitButton = document.querySelector('button[type="submit"]');
    const form = document.querySelector('form');

    if (fileInput && questionInput && submitButton && form) {
        submitButton.addEventListener('click', function(event) {
            if (!fileInput.files.length) {
                alert('Please upload a file.');
                event.preventDefault(); // Prevent form submission
            } else if (!questionInput.value.trim()) {
                alert('Please enter your question.');
                event.preventDefault(); // Prevent form submission
            }
            // The form will submit if both file and question are present
        });

        // Optional: Add visual feedback on file selection
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                console.log('Selected file:', this.files[0].name);
                // You could update a label or display the filename here if you add a specific element for it in the HTML
            }
        });

        // Optional: Clear the answer/error message when a new file is uploaded or question is typed
        fileInput.addEventListener('change', function() {
            const answerContainer = document.querySelector('.answer-container');
            const errorMessage = document.querySelector('.error-message');
            if (answerContainer) {
                answerContainer.remove();
            }
            if (errorMessage) {
                errorMessage.remove();
            }
        });

        questionInput.addEventListener('input', function() {
            const answerContainer = document.querySelector('.answer-container');
            const errorMessage = document.querySelector('.error-message');
            if (answerContainer) {
                answerContainer.remove();
            }
            if (errorMessage) {
                errorMessage.remove();
            }
        });
    } else {
        console.error('One or more form elements not found.');
    }
});