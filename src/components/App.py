import streamlit as st
import pandas as pd
import joblib
import numpy as np
import datetime
import os

# --- 1. SET UP THE PAGE ---
st.set_page_config(page_title="Retail Scenario Planner", layout="wide")
st.title("📊 Retail Demand & Scenario Planner")
st.markdown("Enter expected transaction details, weather, and historical data to simulate total sales revenue.")

# --- 2. LOAD PIPELINE COMPONENTS ---
@st.cache_resource
def load_models():
    current_dir=os.path.dirname(os.path.abspath(__file__))
    model_path=os.path.join(current_dir,'Revenue_pipeline_best.joblib')
    
    model=joblib.load(model_path)
    return preprocessor, model

try:
    preprocessor, model = load_models()
    models_loaded = True
except FileNotFoundError:
    st.error("⚠️ Could not find 'preprocessor.joblib' or 'model.joblib'. Please ensure both are in the same folder as this script.")
    models_loaded = False

# --- 3.THE USER INTERFACE ---
if models_loaded:
    with st.form("prediction_form"):
        
        st.subheader("🛒 Scenario Details (What-If Variables)")
        col_t1, col_t2, col_t3, col_t4 = st.columns(4)
        with col_t1:
            quantity = st.number_input("Expected Quantity", min_value=1, value=5, step=1)
        with col_t2:
            unit_price = st.number_input("Unit Price (₹)", min_value=0.0, value=500.0, step=50.0)
        with col_t3:
            discount = st.number_input("Discount (%)", min_value=0.0, max_value=100.0, value=10.0, step=5.0)
        with col_t4:
            customer_count = st.number_input("Expected Customers", min_value=0, value=25, step=1)

        st.markdown("---")
        
        st.subheader("📅 Date & Calendar Information")
        col1, col2, col3 = st.columns(3)
        with col1:
            forecast_date = st.date_input("Select Forecast Date", datetime.date.today())
        with col2:
            season = st.selectbox("Season", ['Summer', 'Monsoon', 'Winter'])
        with col3:
            is_holiday = st.selectbox("Is it a Holiday?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")

        st.markdown("---")
        
        st.subheader("🌤️ Expected Weather")
        col4, col5, col6 = st.columns(3)
        with col4:
            temperature_avg = st.number_input("Average Temperature (°C)", value=25.0, step=0.1)
        with col5:
            rainfall_category = st.selectbox("Rainfall Category", ['None', 'Light', 'Moderate', 'Heavy'])
            
                
        with col6:
            holiday_rainfall = st.number_input("Holiday Rainfall (mm)", value=0.0, step=0.1)

        st.markdown("---")
        
        st.subheader("📉 Historical Data")
        col7, col8 = st.columns(2)
        with col7:
            sales_lag_7 = st.number_input("Sales 7 Days Ago", value=50000.0, step=1000.0)
            sales_lag_14 = st.number_input("Sales 14 Days Ago", value=50000.0, step=1000.0)
        with col8:
            rolling_avg_7 = st.number_input("7-Day Rolling Average", value=50000.0, step=1000.0)
            rolling_avg_14 = st.number_input("14-Day Rolling Average", value=50000.0, step=1000.0)

        submit_button = st.form_submit_button(label="Calculate Expected Revenue")

    # --- 4. PREDICTION LOGIC ---
    if submit_button:
        year = forecast_date.year
        month = forecast_date.month
        day = forecast_date.day
        day_of_week = forecast_date.weekday() 
        is_weekend = 1 if day_of_week >= 5 else 0
        quarter = (month - 1) // 3 + 1
        
        weekend_holiday = 1 if (is_weekend == 1 and is_holiday == 1) else 0


        input_data = {
            'Quantity': [quantity],
            'Unit Price': [unit_price],
            'Discount': [discount],
            'Year': [year],
            'Month': [month],
            'Day': [day],
            'DayOfWeek': [day_of_week],
            'IsWeekend': [is_weekend],
            'Quarter': [quarter],
            'Sales_Lag_7': [sales_lag_7],
            'Sales_Lag_14': [sales_lag_14],
            'Rolling_Avg_7': [rolling_avg_7],
            'Rolling_Avg_14': [rolling_avg_14],
            'Customer_Count': [customer_count],
            'Is_Holiday': [is_holiday],
            'Temperature_Avg': [temperature_avg],
            'Weekend_Holiday': [weekend_holiday],
            'Holiday_Rainfall': [holiday_rainfall],
            'Season': [season],
            'Rainfall_Category': [rainfall_category]
        }
        try:
            expected_features = [
                'Quantity', 'Unit Price', 'Discount', 'Year', 'Month', 'Day', 
                'DayOfWeek', 'IsWeekend', 'Quarter', 'Sales_Lag_7', 'Sales_Lag_14',
                'Rolling_Avg_7', 'Rolling_Avg_14', 'Customer_Count',
                'Is_Holiday', 'Temperature_Avg', 'Weekend_Holiday', 
                'Holiday_Rainfall', 'Season', 'Rainfall_Category'
            ]
            
            
        except Exception as e:
            st.error(f"Error during prediction: {e}")

        input_df = pd.DataFrame(input_data)

        input_df = input_df[expected_features]


        try:
            
            prediction = model.predict(input_df)[0]

            st.success("✅ Scenario Calculated Successfully!")
            st.metric(label="Projected Total Sales Revenue", value=f"₹ {prediction:,.2f}")
            stock=prediction*1.65
            st.metric(label="Predicted Safe Stocks", value=f"₹ {stock:,.2f}")
            
        except Exception as e:
            st.error(f"Error during prediction: {e}")
            st.info("If it still fails, please copy and paste the error message above so I can fix it instantly!")