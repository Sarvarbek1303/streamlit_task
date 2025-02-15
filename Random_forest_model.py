import streamlit as st
import numpy as np
import joblib

# Load the trained Random Forest model
model = joblib.load("Random_Forest_Model.pkl")

# Initialize MAPE variable
mape = 0  # Default value to avoid NameError. This could be computed or read from a file.

# Try to read MAPE value from file if available
try:
    with open("MAPE.txt", "r") as f:
        mape_value = f.read().strip()  # Read content and remove leading/trailing spaces
        if mape_value:  # Check if the value is not empty
            mape = float(mape_value)  # Convert to float if it's a valid number
        else:
            mape = "N/A"  # If the file is empty, set MAPE to "N/A"
except FileNotFoundError:
    mape = "N/A"  # If the file doesn't exist, set MAPE to "N/A"

# Streamlit UI
st.title("📊 Stiker sotuvini bashorat qilish (Random Forest)")
st.write("Ma'lumotlarni kiriting va natijani oling!")

# Display MAPE in the sidebar
st.sidebar.write(f"### MAPE: {mape}%")

# Dictionary for categorical encoding (if needed)
category_mappings = {
    "country": {"USA": 0, "Canada": 1, "Germany": 2},  # Example categories, replace with actual ones
    "store": {"Store_A": 0, "Store_B": 1, "Store_C": 2},
    "product": {"Product_X": 0, "Product_Y": 1, "Product_Z": 2}
}

# Feature names
feature_names = ['country', 'store', 'product', 'year', 'month', 'day', 'weekday', 'weekofyear']

# Collect user input
input_data = []
for feature in feature_names:
    if feature in category_mappings:
        value = st.selectbox(f"Tanlang {feature}:", list(category_mappings[feature].keys()))
        input_data.append(category_mappings[feature][value])  # Convert text to numerical value
    else:
        value = st.number_input(f"Enter value for {feature}", step=1)
        input_data.append(value)

# Predict when button is clicked
if st.button("🔍 Bashorat qilish"):
    # Convert input data to NumPy array and reshape for the model
    input_array = np.array([input_data])

    # Make prediction
    prediction = model.predict(input_array)[0]  # Correct variable name here

    # Display result
    st.success(f"📈 Bashorat qilingan stiker sotuvlari: **{prediction:.2f}** dona")

