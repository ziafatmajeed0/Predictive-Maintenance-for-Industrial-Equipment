import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Load the trained model
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Load feature names
with open('features.pkl', 'rb') as feature_file:
    feature_names = pickle.load(feature_file)

st.title('Predictive Maintenance: Equipment Condition Classifier')

# Input fields for sensor readings
temperature_input = st.number_input('Temperature (°C)', min_value=0.0, value=75.0, step=0.1)
vibration_input = st.number_input('Vibration (mm/s)', min_value=0.0, value=5.0, step=0.1)
pressure_input = st.number_input('Pressure (bar)', min_value=0.0, value=1.0, step=0.01)
rpm_input = st.number_input('RPM', min_value=500.0, value=1500.0, step=50.0)
hour_input = st.number_input('Hour of the Day', min_value=0, max_value=23, value=12)
dayofweek_input = st.number_input('Day of Week (0=Monday, 6=Sunday)', min_value=0, max_value=6, value=3)

# Create query DataFrame
query_data = pd.DataFrame({
    'Temperature': [temperature_input],
    'Vibration': [vibration_input],
    'Pressure': [pressure_input],
    'RPM': [rpm_input],
    'Hour': [hour_input],
    'DayOfWeek': [dayofweek_input]
})

# Ensure columns are in the correct order
query_data = query_data[feature_names]

# Predict condition
if st.button('Predict Condition'):
    prediction = model.predict(query_data)[0]
    st.subheader(f'Predicted Equipment Condition: **{prediction}**')

    if prediction == "Normal":
        st.success("✅ The equipment is operating normally.")
    elif prediction == "Warning":
        st.warning("⚠️ Warning: The equipment might need maintenance soon.")
    elif prediction == "Critical":
        st.error("🚨 Critical: Immediate maintenance required!")
