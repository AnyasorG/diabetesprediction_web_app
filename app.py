from flask import Flask, request, jsonify, render_template
from model import predict_diabetes

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Collect inputs from form (as strings)
        user_input = {
            'Age': request.form['Age'],
            'PhysicallyActive': request.form['PhysicallyActive'],
            'BMI': float(request.form['BMI']),
            'Sleep': float(request.form['Sleep']),
            'SoundSleep': float(request.form['SoundSleep']),
            'JunkFood': request.form['JunkFood'],
            'Stress': request.form['Stress'],
            'BPLevel': request.form['BPLevel'],
            'Pregnancies': int(request.form['Pregnancies']),
            'UrinationFreq': request.form['UrinationFreq'],
            'Gender': request.form['Gender'],
            'FamilyDiabetes': request.form['FamilyDiabetes'],
            'Smoking': request.form['Smoking'],
            'Alcohol': request.form['Alcohol'],
            'RegularMedicine': request.form['RegularMedicine'],
            'GDiabetes': request.form['GDiabetes'],
        }

        # Debugging: Print user input
        print("Received data for prediction:", user_input)

        # Call the model prediction function
        result = predict_diabetes(user_input)

        # Return the result as JSON
        return jsonify({'prediction': result})

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error during prediction: {str(e)}")
        return jsonify({'error': 'An error occurred during prediction. Please try again.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
