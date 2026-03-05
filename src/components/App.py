import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os
import plotly.express as px

# --- 1. SET UP THE PAGE ---
st.set_page_config(page_title="Hyperlocal Demand Forecasting System", layout="wide")
st.title("📊 Hyperlocal Demand Forecasting System")
st.markdown("Enter transaction details and environmental factors to simulate projected revenue.")

# --- 2. LOAD THE PIPELINE ---
@st.cache_resource
def load_model():
    # We only need the main pipeline because it contains the preprocessor internally
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, 'Revenue_pipeline_best.joblib')
    model = joblib.load(model_path)
    return model

try:
    model = load_model()
    models_loaded = True
except FileNotFoundError:
    st.error("⚠️ Could not find 'Revenue_pipeline_best.joblib'. Please ensure it is in the same folder as this script.")
    models_loaded = False

# --- 3. HELPER FUNCTION: FEATURE IMPORTANCE ---
def plot_importance(pipeline):
    # Extracting components from the pipeline
    # Index 0 is the ColumnTransformer, Index -1 is the Regressor
    regressor = pipeline.steps[-1][1]
    preprocessor = pipeline.steps[0][1]

    # Get expanded feature names (e.g., Season_Winter)
    feature_names = preprocessor.get_feature_names_out()
    importances = regressor.feature_importances_

    feat_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
    feat_df = feat_df.sort_values(by='Importance', ascending=True).tail(15)

    fig = px.bar(feat_df, x='Importance', y='Feature', orientation='h',
                 title="Top 15 Revenue Drivers", color='Importance',
                 color_continuous_scale='Viridis')
    return fig

# --- 4. BUILD THE USER INTERFACE ---
if models_loaded:
    tab1, tab2 = st.tabs(["Revenue Predictor", "Model Insights"])

    with tab1:
        with st.form("prediction_form"):
            st.subheader("🛒 Scenario Details")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                quantity = st.number_input("Quantity", min_value=1, value=2)
                unit_price = st.number_input("Unit Price (₹)", min_value=1.0, value=500.0)
                discount = st.slider("Discount (%)", 0, 50, 5)
            
            with col2:
                year = st.selectbox("Year", [2024, 2025, 2026])
                month = st.slider("Month", 1, 12, 10)
                day = st.slider("Day", 1, 31, 15)
            
            with col3:
                customer_count = st.number_input("Expected Customer Count", value=50)
                temperature_avg = st.number_input("Avg Temperature (°C)", value=25.0)

            st.subheader("📈 Historical & Contextual Data")
            col4, col5, col6 = st.columns(3)
            
            with col4:
                sales_lag_7 = st.number_input("Sales Lag (7 Days)", value=10000.0)
                sales_lag_14 = st.number_input("Sales Lag (14 Days)", value=9500.0)
                rolling_avg_7 = st.number_input("Rolling Avg (7 Days)", value=10500.0)
                rolling_avg_14 = st.number_input("Rolling Avg (14 Days)", value=10200.0)

            with col5:
                season = st.selectbox("Season", ["Winter", "Summer", "Monsoon", "Spring"])
                rainfall_category = st.selectbox("Rainfall Category", ["None", "Light", "Moderate", "Heavy"])
                # Note: 'None' is passed as a string, matching your training data categories.

            with col6:
                is_holiday = st.checkbox("Is it a Holiday?")
                weekend_holiday = st.checkbox("Is it a Weekend Holiday?")
                holiday_rainfall = st.number_input("Holiday Rainfall (mm)", value=0.0)

            submit_button = st.form_submit_button(label="Calculate Expected Revenue")

        if submit_button:
            # Derived features
            day_of_week = 0 # Placeholder logic for simplicity
            is_weekend = 1 if day_of_week >= 5 else 0
            quarter = (month - 1) // 3 + 1

            # 1. Create Dataframe with EXACTLY 20 features in the trained order
            input_data = {
                'Quantity': [quantity], 'Unit Price': [unit_price], 'Discount': [discount],
                'Year': [year], 'Month': [month], 'Day': [day],
                'DayOfWeek': [day_of_week], 'IsWeekend': [is_weekend], 'Quarter': [quarter],
                'Sales_Lag_7': [sales_lag_7], 'Sales_Lag_14': [sales_lag_14],
                'Rolling_Avg_7': [rolling_avg_7], 'Rolling_Avg_14': [rolling_avg_14],
                'Customer_Count': [customer_count], 'Is_Holiday': [1 if is_holiday else 0],
                'Temperature_Avg': [temperature_avg], 'Weekend_Holiday': [1 if weekend_holiday else 0],
                'Holiday_Rainfall': [holiday_rainfall], 'Season': [season],
                'Rainfall_Category': [rainfall_category]
            }
            
            input_df = pd.DataFrame(input_data)

            try:
                # 2. Feed raw dataframe directly to the pipeline
                prediction = model.predict(input_df)[0]
                
                st.success("✅ Prediction Complete")
                st.metric(label="Projected Total Sales Revenue", value=f"₹ {prediction:,.2f}")
                st.metric(label="Projected Safety Stocks", value=f"₹ {prediction*1.26:,.2f}")
            except Exception as e:
                st.error(f"Error during prediction: {e}")

    with tab2:
        st.subheader("Model Interpretation")
        st.plotly_chart(plot_importance(model), use_container_width=True)