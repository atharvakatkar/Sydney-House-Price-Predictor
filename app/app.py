# LIBRARIES
import streamlit as st
import joblib
import numpy as np
import pandas as pd

# LOAD MODEL
model = joblib.load("models/best_rf_model.pkl")

# PAGE CONFIG
st.set_page_config(
    page_title="Sydney House Price Predictor",
    page_icon="🏡",
    layout="centered"
)

st.title("🏡Sydney House Price Predictor")
st.markdown("Estimate residential property prices across Sydney using ML")
st.divider()

# INPUT FORM
col1, col2, col3 = st.columns(3)

with col1:
    num_bed = st.number_input("Bedrooms", min_value=1, max_value=10, value=1)
    num_bath = st.number_input("Bathrooms", min_value=1, max_value=10, value=1)
with col2:
    num_parking = st.number_input("Parking Spaces", min_value=0, max_value=5, value=1)
    property_size = st.number_input("Property Size (sqm)", min_value=50.00, max_value=5000.00, value=50.00)
with col3:
    km_from_cbd = st.number_input("Distance from CBD (km)", min_value=0.00, max_value=100.00, value=5.00)
    time_to_cbd = st.number_input("Time to CBD via Public Transport (mins)", min_value=0.00, max_value=300.00, value=15.00)

st.divider()

# INPUT FORM
col4, col5 = st.columns(2)

with col4:
    suburb_population = st.number_input("Suburb Population", min_value=50, max_value=100000, value=500)
    suburb_median_income = st.number_input("Suburb Median Income (AUD$)", min_value=20000, max_value=2000000, value=50000)
with col5:
    property_inflation = st.number_input("Property Inflation Index", min_value=0.0, max_value=5.0, value=1.0)
    median_apartment_price = st.number_input("Suburb Median Apartment Price (2020) ($)", min_value=100000, max_value=5000000, value=700000)

st.divider()

property_type = st.selectbox(
    "Property Type",
    ["Apartment (Base)", "House", "Land", "Off Plan Apartment", "Off Plan House", "Other"]
)

# PREDICT BUTTON
if st.button("Predict Price", type="primary"):

    # LOG TRANSFORMATIONS
    log_property_size = np.log1p(property_size)
    log_suburb_population = np.log1p(suburb_population)
    log_median_apartment_price = np.log1p(median_apartment_price)
    log_suburb_median_income = np.log1p(suburb_median_income)

    # INTERACTION FEATURES
    bed_x_size = num_bed * log_property_size
    bath_x_size = num_bath * log_property_size
    income_x_distance = log_suburb_median_income * km_from_cbd
    parking_x_income = num_parking * log_suburb_median_income

    # PROPERTY TYPE ENCODING
    is_house = 1 if property_type == "House" else 0
    is_land = 1 if property_type == "Land" else 0
    is_off_plan_apartment = 1 if property_type == "Off Plan Apartment" else 0
    is_off_plan_house = 1 if property_type == "Off Plan House" else 0
    is_other = 1 if property_type == "Other" else 0

    # BUILD INPUT DATAFRAME
    input_data = pd.DataFrame([{
        "Num Bath": num_bath,
        "Num Bed": num_bed,
        "Num Parking": num_parking,
        "Property Size": log_property_size,
        "Suburb Population": log_suburb_population,
        "Suburb Median Income": log_suburb_median_income,
        "Property Inflation Index": property_inflation,
        "Km From Cbd": km_from_cbd,
        "Median Apartment Price (2020)": log_median_apartment_price,
        "Time To Cbd (Public Transport) [Town Hall St]": time_to_cbd,
        "Is House": is_house,
        "Is Land": is_land,
        "Is Off Plan Apartment": is_off_plan_apartment,
        "Is Off Plan House": is_off_plan_house,
        "Is Other": is_other,
        "Bed X Size": bed_x_size,
        "Bath X Size": bath_x_size,
        "Income X Distance": income_x_distance,
        "Parking X Income": parking_x_income
    }])

    # PREDICT
    log_prediction = model.predict(input_data)[0]
    predicted_price = np.expm1(log_prediction)

    # DISPLAY RESULT
    st.success(f"### Estimated Property Price: ${predicted_price:,.0f}")
    st.caption("Prediction based on Random Forest model trained on Sydney property data. For indicative purposes only.")