import tensorflow as tf
import pandas as pd
import numpy as np
import joblib

# Load the trained model
model = tf.keras.models.load_model('best_model.keras')

# Load the scaler (if you used one during training)
scaler = joblib.load('scaler.pkl')

def predict_diabetes(input_data):
    try:
        # Convert input_data into a DataFrame
        input_df = pd.DataFrame([input_data])

        # Specific mappings as per your preprocessing during training
        # Mapping dictionaries
        age_mapping = {'less than 40': 0, '40-49': 1, '50-59': 2, '60 or older': 3}
        physical_activity_mapping = {
            'none': 0,
            'less than half an hr': 1,
            'more than half an hr': 2,
            'one hr or more': 3
        }
        junk_food_mapping = {
            'occasionally': 0,
            'often': 1,
            'very often': 2,
            'always': 3
        }
        stress_mapping = {
            'not at all': 0,
            'sometimes': 1,
            'very often': 2,
            'always': 3
        }
        bp_level_mapping = {
            'low': 0,
            'normal': 1,
            'high': 2
        }
        urination_freq_mapping = {
            'not much': 0,
            'quite often': 1
        }
        gender_mapping = {'female': 0, 'male': 1}
        
        # Mapping for yes/no binary features
        yes_no_mapping = {'no': 0, 'yes': 1}

        # Apply mappings to the input data
        input_df['Age'] = input_df['Age'].map(age_mapping)
        input_df['PhysicalActivityLevel'] = input_df['PhysicallyActive'].map(physical_activity_mapping)
        input_df['JunkFoodFrequency'] = input_df['JunkFood'].map(junk_food_mapping)
        input_df['StressLevel'] = input_df['Stress'].map(stress_mapping)
        input_df['BloodPressureLevel'] = input_df['BPLevel'].str.strip().str.lower().map(bp_level_mapping)
        input_df['UrinationFrequency'] = input_df['UrinationFreq'].map(urination_freq_mapping)
        input_df['Gender'] = input_df['Gender'].map(gender_mapping)

        # Apply yes/no mappings
        input_df['FamilyDiabetes'] = input_df['FamilyDiabetes'].map(yes_no_mapping)
        input_df['Smoking'] = input_df['Smoking'].map(yes_no_mapping)
        input_df['AlcoholConsumption'] = input_df['Alcohol'].map(yes_no_mapping)
        input_df['RegularMedicineUse'] = input_df['RegularMedicine'].map(yes_no_mapping)
        input_df['GestationalDiabetes'] = input_df['GDiabetes'].map(yes_no_mapping)

        # Ensure the mappings are applied
        if input_df.isnull().any().any():
            raise ValueError("Error in mapping categorical features. Possible unknown category in input.")

        # Ensure all expected columns are present
        expected_columns = [
            'Age', 'PhysicalActivityLevel', 'BMI', 'Sleep', 'SoundSleep', 'JunkFoodFrequency',
            'StressLevel', 'BloodPressureLevel', 'Pregnancies', 'UrinationFrequency',
            'Gender', 'FamilyDiabetes', 'Smoking',
            'AlcoholConsumption', 'RegularMedicineUse', 'GestationalDiabetes'
        ]

        # Add missing columns with default value 0
        for col in expected_columns:
            if col not in input_df.columns:
                input_df[col] = 0

        # Reorder columns to match the model's expectation
        input_df = input_df[expected_columns]

        # Convert data types to float for model input
        input_df = input_df.astype(float)

        # Apply scaling
        input_scaled = scaler.transform(input_df)

        # Make prediction using the trained model
        prediction = model.predict(input_scaled)

        # Interpret the result
        result = "Diabetic" if prediction[0][0] > 0.5 else "Not Diabetic"
        return result

    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        return "An error occurred. Please try again."
