# SARIMA Forecasting – Car Sales in Quebec

This project was completed as part of the **Time Series Analysis course** in the **Master of Analytics program at RMIT University**.

## Objective
Analyse monthly car sales in Quebec (1960–1968) and build a seasonal time series model to forecast future sales.

## Dataset
The dataset contains **monthly car sales observations from 1960 to 1968**.

## Tools Used
- R
- forecast package
- TSA
- tseries
- fUnitRoots

## Methodology

The analysis included:

- Descriptive time series analysis
- Lag correlation analysis
- ACF and PACF analysis
- Normality testing (Shapiro-Wilk)
- Stationarity testing (ADF, KPSS, Phillips-Perron)
- Box-Cox transformation
- SARIMA model specification
- Model comparison using AIC, BIC, and error measures
- Residual diagnostics

## Model Selection

Several SARIMA models were evaluated. The best model selected was:

SARIMA(1,0,2) × (2,1,1)₁₂

This model was chosen based on:

- Lowest forecasting error
- Residual diagnostics
- Statistical significance of parameters

## Forecasting

The final model was used to forecast **10 months ahead**, predicting car sales from **January 1969 to October 1969**.

