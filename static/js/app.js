document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('prediction-form');
    const resultDiv = document.getElementById('prediction-result');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(form);

        fetch('/predict', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.prediction) {
                resultDiv.innerHTML = `<h2>Prediction Result: ${data.prediction}</h2>`;
                
                // Apply modern styles conditionally
                if (data.prediction === 'Diabetic') {
                    resultDiv.classList.add('diabetic');
                } else {
                    resultDiv.classList.remove('diabetic');
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            resultDiv.innerHTML = `<h2>An error occurred. Please try again.</h2>`;
        });
    });
});
