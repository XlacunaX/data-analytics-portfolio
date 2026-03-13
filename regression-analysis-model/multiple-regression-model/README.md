# Multiple Regression Analysis – Drug Retention & Crest Sales

This project was completed as part of the **Regression Analysis course (MATH1312)** in the **Master of Analytics program at RMIT University**.

## Objective
Apply multiple linear regression techniques to analyse relationships between predictors and response variables using statistical modelling in R.

## Datasets

Two datasets were analysed:

### 1. Drug Retention in Rat Liver
Predict the **percentage of drug retained in the liver (Y)** using:

- X1: Body weight of the rat  
- X2: Liver weight  
- X3: Dose administered  

### 2. Crest Toothpaste Sales
Analyse factors affecting **toothpaste sales** using:

- x1: Advertising budget  
- x2: Sales ratio  
- x3: Disposable income  

## Tools Used
- R
- RStudio
- ggplot2
- GGally
- car package
- Statistical inference techniques

## Methods

The following techniques were applied:

- Multiple Linear Regression
- ANOVA (F-tests)
- t-tests for coefficient significance
- Multicollinearity detection (Correlation matrix, VIF)
- Residual diagnostics
- Model selection techniques:
  - Forward selection
  - Backward elimination
  - Stepwise regression

## Key Insights

- In the **drug retention model**, dose and body weight were significant predictors.
- Backward elimination produced a reduced model with **body weight and dose** as predictors.
- In the **Crest sales model**, disposable income was the most influential predictor.
- The final regression model explained **approximately 97% of the variance in sales (R² ≈ 0.97)**. :contentReference[oaicite:1]{index=1}
- Residual diagnostics confirmed most regression assumptions were satisfied.
