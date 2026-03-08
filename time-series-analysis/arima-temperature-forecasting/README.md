# ARIMA Time Series Forecasting – Global Temperature Analysis

This project was completed as part of the **Time Series Analysis course** in the **Master of Analytics program at RMIT University**.

## Objective
Analyse global land temperature anomalies from 1850–2023 and develop ARIMA models to forecast future temperature patterns.

## Dataset
The dataset contains **yearly global land temperature anomalies** measured in degrees Celsius from **1850 to 2023**.

## Tools Used
- R
- TSA
- forecast
- tseries
- fUnitRoots

## Methodology

The following steps were performed:

1. Descriptive analysis of the temperature time series
2. Stationarity testing using:
   - Augmented Dickey–Fuller (ADF)
   - KPSS test
   - Phillips–Perron test
3. Data transformation using **Box-Cox transformation**
4. First differencing to achieve stationarity
5. Identification of candidate ARIMA models using:
   - ACF and PACF plots
   - EACF plot
   - BIC table
6. Model estimation using:
   - CSS
   - ML
   - CSS-ML
7. Model comparison using:
   - AIC
   - BIC
   - RMSE
   - MAE

## Model Selection

Based on parameter significance and model diagnostics, the best models identified were:

- **ARIMA(1,1,3)**
- **ARIMA(2,1,0)**

## Key Insights

- The temperature anomaly series shows a **long-term upward trend**.
- The original series was **non-stationary**.
- After **first differencing**, the series became stationary.
- ARIMA models successfully captured the temporal structure.

