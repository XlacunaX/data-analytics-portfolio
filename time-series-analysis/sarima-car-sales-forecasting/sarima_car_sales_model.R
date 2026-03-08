rm(list=ls())
install.packages("TSA")
library(TSA)
install.packages("fUnitRoots")
library(fUnitRoots)
install.packages("FSAdata")
library(FSAdata)
library(tseries)
library(lmtest)
library(forecast)
library(dplyr)

# Function for sorting AIC and BIC output
sort.score <- function(x, score = c("bic", "aic")){
  if (score == "aic"){
    x[with(x, order(AIC)),]
  } else if (score == "bic") {
    x[with(x, order(BIC)),]
  } else {
    warning('score = "x" only accepts valid arguments ("aic","bic")')
  }
}

# Stationarity test function
stationarity_tests <- function(data) {
  
  adf_result <- adf.test(data)
  cat("Augmented Dickey-Fuller (ADF) Test:\n")
  print(adf_result)
  
  kpss_result <- kpss.test(data)
  cat("\nKwiatkowski-Phillips-Schmidt-Shin (KPSS) Test:\n")
  print(kpss_result)
  
  pp_result <- pp.test(data)
  cat("\nPhillips-Perron (PP) Test:\n")
  print(pp_result)
}

# Function for residual analysis
diagnostic_plots <- function(model) {
  # Set up the plotting area
  par(mfrow = c(3, 2))
  
  # Standardized Residuals Plot
  plot(rstandard(model),
       ylab = 'Standardized Residuals', type = 'o',
       main = "Residuals from the ARIMA Model")
  abline(h = 0)
  
  # Histogram of Standardized Residuals
  hist(rstandard(model), xlab = 'Standardized Residuals',
       main = "Histogram of Residuals from the ARIMA Model")
  
  # Q-Q Plot for Residuals
  qqnorm(rstandard(model), main = "Q-Q plot for Residuals: ARIMA Model")
  qqline(rstandard(model))
  
  # Shapiro-Wilk Normality Test
  shapiro_result <- shapiro.test(rstandard(model))
  print(shapiro_result)
  
  # ACF of Residuals
  acf(rstandard(model), lag.max = 36,
      main = "ACF of Residuals from the ARIMA Model")
  
  # PACF of Residuals
  pacf(rstandard(model), lag.max = 36,
       main = "PACF of Residuals from the ARIMA Model")
  
  # Ljung-Box Test
  ljung_box_result <- Box.test(rstandard(model), type = "Ljung-Box")
  print(ljung_box_result)
  
  # Time Series Diagnostic Plots
  tsdiag(model, gof = 15, omit.initial = FALSE)
}

# Function for coef test
fit_sarima_models <- function(ts_data, orders, seasonal_orders, period) {
  
  # Define a helper function to fit and test a model
  fit_and_test <- function(order, seasonal_order, method) {
    tryCatch({
      model <- Arima(ts_data, order=order, seasonal=list(order=seasonal_order, period=period), method=method)
      test_results <- coeftest(model)
      return(test_results)
    }, error = function(e) {
      cat("Error fitting model with order =", paste(order, collapse=","),
          "and seasonal order =", paste(seasonal_order, collapse=","), 
          "using method =", method, "\n")
      return(NULL)
    })
  }
  
  # Initialize a list to store results
  results <- list()
  
  # Loop through each combination of orders and methods
  for (order in orders) {
    for (seasonal_order in seasonal_orders) {
      for (method in c("ML", "CSS", "CSS-ML")) {
        model_name <- paste0("SARIMA(", paste(order, collapse=","), ")x(", paste(seasonal_order, collapse=","), ")_", period, ".", method)
        cat("\nFitting model:", model_name, "\n")
        results[[model_name]] <- fit_and_test(order, seasonal_order, method)
      }
    }
  }
  
  return(results)
}


# Loading the dataset
setwd("C:/Users/shamb/OneDrive/Desktop/Time Series Analysis/Assignment 3")
data <- read.csv("monthlycarsales.csv")


head(data)
summary(data)
class(data)
plot(data, type='o', ylab= 'sales',xlab= 'Year', main="Cars Sales in Quebec", col="blue")

# Converting data in a time series object
Car_SalesTS <- ts(data$Monthly.car.sales.in.Quebec.1960.1968, start = c(1960,1),
                    end = c(1968,12), frequency = 12)


# Descriptive Analysis
class(Car_SalesTS)
summary(Car_SalesTS)
plot(Car_SalesTS, type = 'o', ylab = 'Car Sales', xlab = 'Year',
     main = "Car Sales in Quebec",
     col = "maroon", pch = 15)


# Creating first lag
orig = Car_SalesTS 
l = zlag(Car_SalesTS) 
index = 2:length(orig)
cor(orig[index],l[index]) 

# Creating second lag
l2 = zlag(zlag(Car_SalesTS))
index = 3:length(l2)
cor(orig[index],l2[index]) 

# ACF plot of lags
acf(Car_SalesTS, lag.max = 80)

# Create a scatter plot
plot(x = l[-1], y = Car_SalesTS[-1], xlab = "Lag", ylab = "Car_SalesTS", col= "green",
     main = "Scatter Plot of Correlations between Lags")
# Add second lag to the plot
points(l2[-c(1, 2)], Car_SalesTS[-c(1, 2)], col = "blue")
legend("topleft", legend = c("First Lag (l)", "Second Lag (l2)"), col = c("green", "blue"), pch = 1)

par(mfrow=c(1,2))
acf(Car_SalesTS, lag.max=80, main ="ACF plot of Car Sales series.")
pacf(Car_SalesTS, lag.max=80, main ="PACF plot of Car Sales series.")
par(mfrow=c(1,1))

# QQ line
qqnorm(Car_SalesTS, ylab='Total Passengers', xlab='Normal Score'
       , main= "QQ Plot of car sales Time Series", col="cornsilk4")
qqline(Car_SalesTS, col = "darkgreen")

# Shapiro Wilk Test
shapiro.test(Car_SalesTS)

# Unitroot Test of the car sales Series
stationarity_tests(Car_SalesTS)

graphics.off()

# Box-Cox Transformation on the time series to minimize changing variance
BC = BoxCox.ar(Car_SalesTS)
title(main= "Log-likelihood Vs Values of Lambda for car sales Series")
BC$ci
lambda <- BC$lambda[which(max(BC$loglike) == BC$loglike)]
lambda
Car_SalesTS_BC = (Car_SalesTS^lambda-1)/lambda

par(mfrow=c(2,1))
plot(Car_SalesTS_BC, type = 'o', ylab = 'Car Sales', xlab = 'Year',
     main = "Transformed Time series plot of Car Sales",
     col = "Blue", pch = 10)
plot(Car_SalesTS, type = 'o', ylab = 'Car Sales', xlab = 'Year',
     main = "Time series plot of Car Sales",
     col = "maroon", pch = 10)

# QQ line
par(mforw=c(2,1))
qqnorm(Car_SalesTS_BC, ylab="Box-Cox GlobalTemp_ts", xlab="Normal Scores",
       col= 'darkcyan',
       main="QQ Plot of Transformed Global Temperature Time Series")
qqline(Car_SalesTS_BC, col = 'darkred')
qqnorm(Car_SalesTS, ylab='Total Passengers', xlab='Normal Score'
       , main= "QQ Plot of US Air Passengers Time Series", col="cornsilk4")
qqline(Car_SalesTS, col = "darkgreen")

# Shapiro Wilk Test
shapiro.test(Car_SalesTS_BC)

# Stationarity test of transformed series
stationarity_tests(Car_SalesTS_BC)

par(mfrow=c(1,2))
acf(Car_SalesTS_BC, lag.max=80, main ="ACF plot")
pacf(Car_SalesTS_BC,lag.max=80, main ="PACF plot")

graphics.off()

m1.car_sales = Arima(Car_SalesTS_BC,order=c(0,0,0),seasonal=list(order=c(0,1,0), period=12))
res.m1 = residuals(m1.car_sales);  
par(mfrow=c(1,1))
plot(res.m1,xlab='Time',ylab='Residuals',main="Time series plot of the residuals")
par(mfrow=c(1,2))
acf(res.m1, lag.max = 80, main = "The sample ACF of the residuals")
pacf(res.m1, lag.max = 80, main = "The sample PACF of the residuals")

m2.car_sales = Arima(Car_SalesTS_BC,order=c(0,0,0),seasonal=list(order=c(1,1,1), period=12))
res.m2 = residuals(m2.car_sales);  
par(mfrow=c(1,1))
plot(res.m2,xlab='Time',ylab='Residuals',main="Time series plot of the residuals")
par(mfrow=c(1,2))
acf(res.m2, lag.max = 80, main = "The sample ACF of the residuals")
pacf(res.m2, lag.max = 80, main = "The sample PACF of the residuals")

m3.car_sales = Arima(Car_SalesTS_BC,order=c(0,0,0),seasonal=list(order=c(2,1,1), period=12))
res.m3 = residuals(m3.car_sales);  
par(mfrow=c(1,1))
plot(res.m3,xlab='Time',ylab='Residuals',main="Time series plot of the residuals")
par(mfrow=c(1,2))
acf(res.m3, lag.max = 80, main = "The sample ACF of the residuals")
pacf(res.m3, lag.max = 80, main = "The sample PACF of the residuals")

stationarity_tests(res.m3)


# Since the series is coming out to be stationary on the basis of stationarity tests. Hence, ordinary 
# difference d=0.

m4.car_sales = Arima(Car_SalesTS_BC,order=c(2,0,4),seasonal=list(order=c(2,1,1), period=12))
res.m4 = residuals(m4.car_sales);  
par(mfrow=c(1,1))
plot(res.m4,xlab='Time',ylab='Residuals',main="Time series plot of the residuals")
par(mfrow=c(1,2))
acf(res.m4, lag.max = 80, main = "The sample ACF of the residuals")
pacf(res.m4, lag.max = 80, main = "The sample PACF of the residuals")

# From above we find the values of p=2 and q=4.

eacf(res.m3)
# First o not interrupted by x is at (1,1)
# (1,0,1),(1,0,2),(2,0,2)

# The tentative models are specified as 
# SARIMA(1,0,1)x(2,1,1)_12
# SARIMA(1,0,2)x(2,1,1)_12
# SARIMA(2,0,2)X(2,1,1)_12

par(mfrow=c(1,1))
bic_table = armasubsets(y=res.m3,nar=5,nma=5,y.name='p',ar.method='ols')
plot(bic_table)

# (1,0,0), (2,0,0)

# The tentative models is specified as 
# SARIMA(1,0,0)x(2,1,1)_12
# SARIMA(2,0,0)x(2,1,1)_12

# Final specified models
# SARIMA(2,0,4)x(2,1,1)_12
# SARIMA(1,0,1)x(2,1,1)_12
# SARIMA(1,0,2)x(2,1,1)_12
# SARIMA(2,0,2)X(2,1,1)_12
# SARIMA(1,0,0)x(2,1,1)_12
# SARIMA(2,0,0)x(2,1,1)_12


# Parameter Estimation
orders <- list(c(2,0,4), c(1,0,1), c(1,0,2), c(2,0,2), c(1,0,0), c(2,0,0))
seasonal_orders <- list(c(2,1,1))
results <- fit_sarima_models(Car_SalesTS_BC, orders, seasonal_orders, period=12)

# Print results
for (name in names(results)) {
  cat("\nModel:", name, "\n")
  if (!is.null(results[[name]])) {
    print(results[[name]])
  } else {
    cat("No results for this model due to an error.\n")
  }
}


# AIC and BIC score

sc.AIC = AIC(m3_204.salesML, m3_101.salesML, m3_102.salesML, 
             m3_202.salesML, m3_100.salesML, m3_200.salesML)

sc.BIC = BIC(m3_204.salesML, m3_101.salesML, m3_102.salesML, 
             m3_202.salesML, m3_100.salesML, m3_200.salesML)

sort.score(sc.AIC, score = "aic")
sort.score(sc.BIC, score = "bic")

# Error Measure
Sm3_204.sales <- accuracy(m3_204.salesCSS)[1:7]
Sm3_101.sales <- accuracy(m3_101.salesCSS)[1:7]
Sm3_102.sales <- accuracy(m3_102.salesCSS)[1:7]
Sm3_202.sales <- accuracy(m3_202.salesCSS)[1:7]
Sm3_100.sales <- accuracy(m3_100.salesCSS)[1:7]
Sm3_200.sales <- accuracy(m3_200.salesCSS)[1:7]

df.Smodels <- data.frame(rbind( Sm3_204.sales, Sm3_101.sales, Sm3_102.sales, 
                          Sm3_202.sales, Sm3_100.sales, Sm3_200.sales))

colnames(df.Smodels) <- c("ME", "RMSE", "MAE", "MPE", "MAPE", 
                          "MASE", "ACF1")
rownames(df.Smodels) <- c("SARIMA(2,0,4)x(2,1,1)_12","SARIMA(1,0,1)x(2,1,1)_12",
                          "SARIMA(1,0,2)X(2,1,1)_12","SARIMA(2,0,2)x(2,1,1)_12",
                          "SARIMA(1,0,0)x(2,1,1)_12", "SARIMA(2,0,0)X(2,1,1)_12")
round(df.Smodels,  digits = 3)

# Residual Analysis

# SARIMA(2,0,4)x(2,1,1)_12
diagnostic_plots(m3_204.salesML)

# SARIMA(1,0,1)x(2,1,1)_12
diagnostic_plots(m3_101.salesML)

# SARIMA(1,0,2)x(2,1,1)_12
diagnostic_plots(m3_102.salesML)

# SARIMA(2,0,2)X(2,1,1)_12
diagnostic_plots(m3_202.salesML)

# SARIMA(1,0,0)x(2,1,1)_12
diagnostic_plots(m3_100.salesML)
# EW

# SARIMA(2,0,0)x(2,1,1)_12
diagnostic_plots(m3_200.salesML)

# After all the analysis SARIMA(1,0,2)X(2,1,1)_12 is the best model
# We will do over parameterization 

# SARIMA(0,0,2)x(2,1,1)
m3_002.salesML = Arima(Car_SalesTS_BC, order=c(0,0,2), seasonal=list(order=c(2,1,1), period=12), method="ML")
coeftest(m3_002.salesML)

m3_002.salesCSS = Arima(Car_SalesTS_BC, order=c(0,0,2), seasonal=list(order=c(2,1,1), period=12), method="CSS")
coeftest(m3_002.salesCSS)

m3_002.salesCSSML = Arima(Car_SalesTS_BC, order=c(0,0,2), seasonal=list(order=c(2,1,1), period=12), method="CSS-ML")
coeftest(m3_002.salesCSSML)

diagnostic_plots(m3_002.salesCSS)

# SARIMA(1,0,3)x(2,1,1)
m3_103.salesML = Arima(Car_SalesTS_BC, order=c(1,0,3), seasonal=list(order=c(2,1,1), period=12), method="ML")
coeftest(m3_103.salesML)

m3_103.salesCSS = Arima(Car_SalesTS_BC, order=c(1,0,3), seasonal=list(order=c(2,1,1), period=12), method="CSS")
coeftest(m3_103.salesCSS)

m3_103.salesCSSML = Arima(Car_SalesTS_BC, order=c(1,0,3), seasonal=list(order=c(2,1,1), period=12), method="CSS-ML")
coeftest(m3_103.salesCSSML)

diagnostic_plots(m3_103.salesCSS)

graphics.off()


# Forecast for SARIMA(1,0,2)x(2,1,1)_12
m3.CarSales = Arima(Car_SalesTS, order=c(1,0,2),
                   seasonal=list(order=c(2,1,1), period=12), 
                   lambda = 0.8)
future = forecast(m3.CarSales, lambda = 0.8, h = 10)
future
plot(future)


# Model names specified for aic, bic and error measures

# SARIMA(2,0,4)x(2,1,1)_12
m3_204.salesML = Arima(Car_SalesTS_BC, order=c(2,0,4), seasonal=list(order=c(2,1,1), period=12), method="ML")
m3_204.salesCSS = Arima(Car_SalesTS_BC, order=c(2,0,4), seasonal=list(order=c(2,1,1), period=12), method="CSS")
# SARIMA(1,0,1)x(2,1,1)_12
m3_101.salesML = Arima(Car_SalesTS_BC, order=c(1,0,1), seasonal=list(order=c(2,1,1), period=12), method="ML")
m3_101.salesCSS = Arima(Car_SalesTS_BC, order=c(1,0,1), seasonal=list(order=c(2,1,1), period=12), method="CSS")
# SARIMA(1,0,2)X(2,1,1)_12
m3_102.salesML = Arima(Car_SalesTS_BC, order=c(1,0,2), seasonal=list(order=c(2,1,1), period=12), method="ML")
m3_102.salesCSS = Arima(Car_SalesTS_BC, order=c(1,0,2), seasonal=list(order=c(2,1,1), period=12), method="CSS")
# SARIMA(2,0,2)x(2,1,1)_12
m3_202.salesML = Arima(Car_SalesTS_BC, order=c(2,0,2), seasonal=list(order=c(2,1,1), period=12), method="ML")
m3_202.salesCSS = Arima(Car_SalesTS_BC, order=c(2,0,2), seasonal=list(order=c(2,1,1), period=12), method="CSS")
# SARIMA(1,0,0)x(2,1,1)_12
m3_100.salesML = Arima(Car_SalesTS_BC, order=c(1,0,0), seasonal=list(order=c(2,1,1), period=12), method="ML")
m3_100.salesCSS = Arima(Car_SalesTS_BC, order=c(1,0,0), seasonal=list(order=c(2,1,1), period=12), method="CSS")
# SARIMA(2,0,0)x(2,1,1)_12
m3_200.salesML = Arima(Car_SalesTS_BC, order=c(2,0,0), seasonal=list(order=c(2,1,1), period=12), method="ML")
m3_200.salesCSS = Arima(Car_SalesTS_BC, order=c(2,0,0), seasonal=list(order=c(2,1,1), period=12), method="CSS")





