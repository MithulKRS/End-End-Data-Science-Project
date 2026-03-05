📈 Hyper-Local Demand Forecasting Engine

Predictive Inventory Optimization using ECommerce Sales & Cities Weather Proxies
📌 Business Problem
Quick-commerce platforms (Blinkit, Zepto) lose millions annually due to two critical issues:

Stockouts: Under-predicting demand during rain or festivals leads to lost revenue and customer churn.

High Holding Costs: Over-stocking perishable goods leads to wastage and increased warehouse costs.

Goal: Build an end-to-end pipeline that predicts SKU-level demand by integrating "Hyper-local" signals (Weather + Holidays) to optimize inventory reorder points.

A machine learning-driven forecasting system designed to predict daily retail revenue with high precision. This project integrates real-time weather data, holiday seasonality, and historical sales trends into a deployed XGBoost pipeline.🚀 

Project Overview
This project solves the challenge of predicting demand at a "hyper-local" level by accounting for factors that traditional models often miss, such as local weather patterns and regional holidays.

Key Achievements:
Accuracy: Achieved a WAPE of 8.26% (Weighted Absolute Percentage Error).
Deployment: Fully functional Streamlit Dashboard for real-time "What-If" scenario planning.External Integration: Automated feature engineering using the OpenMeteo API for historical and forecasted weather.

🛠️ Tech Stack
Language: Python 3.x
ML Frameworks: Scikit-Learn, XGBoostData 
Manipulation: Pandas, NumPy
Deployment: Streamlit, Joblib 
Environment: Docker (Containerized for scalability)

📊 Features & Engineering
To achieve high accuracy without data leakage, the model utilizes:Temporal Features: Year, Month, Day, Day of Week, IsWeekend, and Quarter.Weather Signals: Average Temperature and Rainfall Categories (mapped from OpenMeteo).Seasonality & Holidays: Interaction features between holidays and weekends to capture peak demand spikes.Lags & Windows: 7-day and 14-day rolling averages and lag features to capture short-term cyclical trends.
📈 Model Performance
Initially, the model showed signs of overfitting due to target leakage. By removing post-transaction variables (like Quantity and Customer_Count during initial training) and implementing TimeSeriesSplit cross-validation, the following realistic metrics were achieved:MetricValue
WAPE   8.26%
MAE    8,531.61
RMSE   11,056.77
Accuracy~ 91.7%💻 

Installation & Usage
1. Clone the Repository
2. Bash:git clone https://github.com/yourusername/hyper-local-demand-forecasting.git
cd hyper-local-demand-forecasting
3. Install Dependencies
4. Bash:pip install -r requirements.txt
5. Run the Streamlit App
6. Bash: streamlit run app.py

🖥️ Dashboard PreviewThe deployed app allows users to input:Date & Calendar info (Auto-calculates Weekends/Quarters).Weather Forecasts (Temperature/Rainfall).Strategic Variables (Price, Discounts, Expected Quantity) to simulate revenue outcomes.📂 Project StructurePlaintext├── data/               # Training and testing datasets
├── models/             # Saved .joblib files (Preprocessor & Model)
├── notebooks/          # Data Exploration and Model Training scripts
├── app.py              # Streamlit Application
├── requirements.txt    # List of dependencies
└── README.md           # Project documentation


👨‍💻 Author:
Mithul Krishna Suresh 
B.Tech in Computer Science and Engineering 
Maulana Azad National Institute of Technology (MANIT), Bhopal
