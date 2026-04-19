# Stock Price Prediction

This project builds a time series model to predict stock prices using historical data obtained from Yahoo Finance.

## 📌 Project Overview

The goal of this project is to develop a predictive model that can estimate future stock prices based on past trends.

This project uses data from Yahoo Finance and applies data preprocessing, visualization, and modeling techniques to understand stock market behavior.

In this case, we are using Stock Market data from "BBCA"

## 📊 Data Source

- Data is collected from **Yahoo Finance**
- Includes historical stock prices such as:
  - Date
  - Open
  - High
  - Low
  - Close
  - Volume

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Prophet
- Matplotlib / Seaborn / Plotly
- Scikit-learn
- yfinance library
- Datetime

## ⚙️ Project Workflow

1. Data Collection from Yahoo Finance
2. Data Cleaning and Preprocessing
4. Feature Engineering (if applicable)
5. Model Training
6. Hypertuning Parameter (if applicable)
7. Model Forecasting
8. Model Evaluation
9. Visualize the results

## 📈 Model Used

- Prophet
- Trained using historical stock price data (Close label)
- Evaluated using common metrics such as MAE, RMSE, or MAPE

## 📉 Results

- Visualization of actual vs predicted stock prices of BBCA
- Model performance metrics
- Insights from prediction trends

## 🚀 How to Run

```bash
# install dependencies
pip install -r requirements.txt

# run notebook or script
python src/main.py
```

## Actual vs Forecast
<img width="846" height="393" alt="image" src="https://github.com/user-attachments/assets/36e7dc7f-ce60-41bd-b612-693ed7678d5e" />

## Components
  ### Time Series Plot
  <img width="989" height="590" alt="image" src="https://github.com/user-attachments/assets/37baa3c4-6b72-437b-aa38-a1a1264198e2" />
  ### Trend and Seasonality
  <img width="894" height="1190" alt="image" src="https://github.com/user-attachments/assets/d19e8505-5922-4c0d-b5d6-e59f40462071" />


  
