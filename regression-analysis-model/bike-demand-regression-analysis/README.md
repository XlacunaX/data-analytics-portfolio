# Bike Demand Forecasting Using Regression Models

This project was completed as part of the **Regression Analysis (MATH1312) course** in the **Master of Analytics program at RMIT University**.

## Objective
Develop regression models to analyse and predict bike rental demand based on seasonal, temporal, and weather-related variables.

## Dataset
The project uses the **Bike Sharing Dataset** from the UCI Machine Learning Repository.

The dataset contains daily bike rental data from the Capital Bikeshare system in Washington D.C. (2011–2012).

Key variables include:

- Season
- Year
- Month
- Holiday indicator
- Weather condition
- Temperature
- Humidity
- Wind speed
- Total bike rentals (target variable)

## Tools Used

- R
- RStudio
- tidyverse
- leaps
- MASS
- nlme
- car

## Methods

Three regression modelling approaches were implemented:

1. **Full Multiple Linear Regression**
2. **Best Subset Regression (Adjusted R² selection)**
3. **Generalised Least Squares (GLS) model with AR(1) correlation**

## Model Evaluation

Models were evaluated using:

- Adjusted R²
- AIC / BIC
- Residual diagnostics
- Durbin–Watson test
- Shapiro–Wilk test
- Variance Inflation Factor (VIF)
- ACF analysis for autocorrelation

## Key Insights

- The regression models explained **over 80% of variation in bike demand**.
- Weather conditions, seasonality, and temperature significantly influence bike rental activity.
- The **GLS model with AR(1) correlation** improved performance by addressing temporal autocorrelation in the data.
