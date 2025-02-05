import streamlit as st
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

# Load the trained CNN-LSTM model
model = load_model("models/cnn_lstm_model.keras")

# Load the training dataset used to fit the scaler
training_data = pd.read_csv("data/processed/finalized_features.csv")

# Fit the StandardScaler on the training dataset
scaler = StandardScaler()
scaler.fit(training_data.drop(columns=["Appliances"]))  # Fit scaler on training features

# Streamlit UI
st.title("Appliance Energy Prediction with CNN-LSTM")
st.write("Enter the relevant inputs to predict energy consumption.")

# Custom CSS for background image
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://www.qpgenergy.co.uk/wp-content/uploads/2022/03/animation-QPG.gif');  
        background-size: cover;
        background-position: center;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# User Input Form for specified features
st.sidebar.header("Input Features")
rolling_mean_6 = st.sidebar.number_input("Rolling Mean 6", value=0.0)
rh_1 = st.sidebar.number_input("RH_1", value=50.0)
rolling_std_6 = st.sidebar.number_input("Rolling Std 6", value=0.0)
appliances_lag_10 = st.sidebar.number_input("Appliances Lag 10", value=100.0)
rolling_std_3 = st.sidebar.number_input("Rolling Std 3", value=0.0)
appliances_lag_30 = st.sidebar.number_input("Appliances Lag 30", value=105.0)

# Convert input into DataFrame with matching feature names
input_data = pd.DataFrame([[rolling_mean_6, rh_1, rolling_std_6, appliances_lag_10, rolling_std_3, appliances_lag_30]], 
                           columns=["rolling_mean_6", "RH_1", "rolling_std_6", "Appliances_lag_10", "rolling_std_3", "Appliances_lag_30"])

# Ensure all required features exist
for col in training_data.drop(columns=["Appliances"]).columns:
    if col not in input_data.columns:
        input_data[col] = 0  # Fill missing features with zero

# Standardize the input data using the fitted scaler
input_scaled = scaler.transform(input_data)
input_scaled = np.expand_dims(input_scaled, axis=1)  # Reshaping for CNN-LSTM input

# Prediction Button
if st.sidebar.button("Predict"):
    prediction = model.predict(input_scaled)
    st.subheader("Prediction Result")
    st.write(f"Predicted Energy Consumption: {prediction[0][0]:.2f} kWh")
