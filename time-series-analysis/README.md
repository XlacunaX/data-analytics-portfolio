# Time Series Analysis – Share Market Investment Forecasting

This project was completed as part of the **Time Series Analysis course** in the **Master of Analytics program at RMIT University**.

## Objective
Analyse a share market trader's investment portfolio time series and build statistical models to forecast future returns.

## Dataset
The dataset contains **179 observations of investment returns** recorded across trading days.

## Tools Used
- R
- TSA package
- Time series regression models

## Methods
The following models were evaluated:

- Linear regression trend model
- Quadratic trend model
- Seasonal model
- Quadratic + Seasonal model
- Harmonic model

## Model Selection
Based on residual diagnostics and model fit:

- The **quadratic model** provided the best balance between fit and generalisation.

## Forecasting
The selected model was used to **forecast the next 5 trading days**.

## Repository Structure
time-series-analysis
│
├── code
│ └── time_series_analysis.R
│
├── data
│ └── assignment1Data2024.csv
│
└── report
└── TIME SERIES ANALYSIS REPORT.pd
