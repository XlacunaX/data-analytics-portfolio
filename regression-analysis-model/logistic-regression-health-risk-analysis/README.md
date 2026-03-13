# Logistic Regression & Pavement Durability Analysis

This project was completed as part of the **Regression Analysis course (MATH1312)** in the **Master of Analytics program at RMIT University**.

## Objective
Apply statistical modelling techniques including multiple linear regression and logistic regression to analyse real-world datasets and evaluate model performance.

## Datasets

Two datasets were analysed:

### 1. Asphalt Pavement Durability
The dataset investigates factors affecting **change in rut depth** in asphalt pavements using six predictors:

- x1: Viscosity  
- x2: % asphalt in surface course  
- x3: % asphalt in base course  
- x4: % fines in surface course  
- x5: % voids in surface course  
- x6: Run indicator  

### 2. Byssinosis Disease Risk
This dataset examines **respiratory disease risk among cotton industry workers**.

Predictors include:

- Dust exposure level  
- Race  
- Sex  
- Smoking status  
- Employment duration  

The response variable indicates whether workers developed **byssinosis**.

## Tools Used

- R
- RStudio
- tidyverse
- car
- leaps
- pROC
- ResourceSelection

## Methods

The analysis included:

- Multiple Linear Regression
- Logistic Regression
- ANOVA testing
- All Possible Subsets Regression
- Residual diagnostics
- Multicollinearity analysis (VIF)
- Model adequacy testing
- ROC curve analysis
- Odds ratio interpretation

## Key Insights

- The asphalt model explained **approximately 72.7% of the variation in rut depth** (R² ≈ 0.73). :contentReference[oaicite:1]{index=1}
- The **run indicator variable** was the most significant predictor in pavement durability.
- Logistic regression identified **dust exposure, smoking status, and employment duration** as major risk factors for byssinosis.
- The model showed good structural fit but limited classification performance (AUC ≈ 0.52). :contentReference[oaicite:2]{index=2}
