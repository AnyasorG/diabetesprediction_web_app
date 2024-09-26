document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('prediction-form');
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission
        const formData = new FormData(form);

        fetch('/predict', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById('prediction-result');
            if (data.prediction) {
                resultDiv.innerHTML = `<h2>Prediction Result: ${data.prediction}</h2>`;
            } else if (data.error) {
                resultDiv.innerHTML = `<h2>Error: ${data.error}</h2>`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            const resultDiv = document.getElementById('prediction-result');
            resultDiv.innerHTML = `<h2>An error occurred. Please try again.</h2>`;
        });
    });
});
