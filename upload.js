document.addEventListener("DOMContentLoaded", function() {
    const uploadForm = document.getElementById("uploadForm");

    uploadForm.addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent default form submission
        
        const formData = new FormData(uploadForm);
        const resultDisplay = document.querySelector('.result');
        resultDisplay.textContent = "Analyzing..."; // Show a message while processing

        // Use fetch to send the data to uploadpy.php
        fetch('uploadpy.php', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text()) // Get the response as text
        .then(data => {
            resultDisplay.textContent = data; // Display the server response in .result
        })
        .catch(error => {
            resultDisplay.textContent = "An error occurred during upload.";
            console.error("Error:", error); // Log any errors for debugging
        });
    });
});
