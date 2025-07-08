# Simple Streamlit Demo for Nino Medical AI
import streamlit as st

st.title("Nino Medical AI Platform - Demo")

st.header("Welcome!")
st.write("This is a demo application showcasing the capabilities of our medical AI platform. All data here is synthetic.")

# Simulated data display
data = {
    "Patient ID": ["001", "002", "003"],
    "Heart Rate": [72, 85, 90],
    "Blood Pressure": ["120/80", "125/85", "130/85"],
    "Condition": ["Stable", "Monitored", "Monitored"]
}

st.subheader("Patient Data")
st.write(data)

# Simulated analysis outcome
st.subheader("Analysis")
st.write("All parameters are within the normal range. No immediate action required.")

# Provide details on how to integrate
st.subheader("Integration Guide")
st.write("Learn more about how to integrate with our medical AI API.")

# Contact information
st.subheader("Contact Us")
st.write("For more information, please reach out to our team.")
