rm(list=ls())
install.packages("TSA")
library(TSA)
install.packages("fUnitRoots")
library(fUnitRoots)
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

# Funtion for coefficient estimation
fit_arima_models <- function(data, orders, methods) {
  results <- list()
  
  for (order in orders) {
    for (method in methods) {
      model <- Arima(data, order = order, method = method)
      test_result <- lmtest::coeftest(model)
      result_name <- paste("model_", paste(order, collapse = ""), "_", method, sep = "")
      results[[result_name]] <- test_result
    }
  }
  
  return(results)
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

# setting up the working directory
setwd("C:/Users/shamb/OneDrive/Desktop/Time Series Analysis/Assignment 2")

# Reading the data file 
GlobalTemp <- read.csv("assignment2data2024.csv")

# View the loaded file
GlobalTemp
head(GlobalTemp)
class(GlobalTemp)
graphics.off()
# Descriptive Analysis
summary(GlobalTemp)
plot(GlobalTemp, type='o', ylab= 'Global Land Temperature Anomalies',xlab= 'Year')

# Convert the dataset into a time series dataset
GlobalTemp_ts <- ts(GlobalTemp$Anomaly, start = min(GlobalTemp$Year),
                    end = max(GlobalTemp$Year), frequency = 1)

# Descriptive Analysis
class(GlobalTemp_ts)
summary(GlobalTemp_ts)
plot(GlobalTemp_ts, type = 'o', ylab = 'Anomaly in Land Temperature', xlab = 'Year',
     main = "Time series plot of Global Land Temperature Anomalies in Degrees Celsius",
     col = "maroon", pch = 15)

# Creating first lag
orig = GlobalTemp_ts 
l = zlag(GlobalTemp_ts) 
index = 2:length(orig)
cor(orig[index],l[index]) 

# Creating second lag
l2 = zlag(zlag(GlobalTemp_ts))
index = 3:length(l2)
cor(orig[index],l2[index]) 

# ACF plot of lags
acf(GlobalTemp_ts, lag.max = 50)

# Create a scatter plot
plot(x = l[-1], y = GlobalTemp_ts[-1], xlab = "Lag", ylab = "GlobalTemp_ts", col= "green",
     main = "Scatter Plot of Correlations between Lags")
# Add second lag to the plot
points(l2[-c(1, 2)], GlobalTemp_ts[-c(1, 2)], col = "blue")
legend("topleft", legend = c("First Lag (l)", "Second Lag (l2)"), col = c("green", "blue"), pch = 1)

# ACF and PACF of the time series
par(mfrow=c(1,2))
acf(GlobalTemp_ts, main ="ACF plot of Global Land Temperature Anomaly series.")
pacf(GlobalTemp_ts, main ="PACF plot of Global Lnad Temperature Anomaly series.")
par(mfrow=c(1,1))

# QQ line
qqnorm(GlobalTemp_ts, ylab='Temperature', xlab='Normal Score'
       , main= "QQ Plot of Global Temperature Time Series", col="cornsilk4")
qqline(GlobalTemp_ts, col = "darkgreen")

# Shapiro Wilk Test
shapiro.test(GlobalTemp_ts)

# Unitroot Test of the Global Temp Series
stationarity_tests(GlobalTemp_ts)

# Box-Cox Transformation on the time series to minimize changing variance
GlobalTempTS <- GlobalTemp_ts + abs(min(GlobalTemp_ts)) + 0.01
BC = BoxCox.ar(GlobalTempTS)
title(main= "Log-likelihood Vs Values of Lambda for Global Temperature Series")
BC$ci
lambda <- BC$lambda[which(max(BC$loglike) == BC$loglike)]
lambda
BC.GlobalTemp_ts = (GlobalTempTS^lambda-1)/lambda

# Plotting the transformed series vs the original series
par(mfrow=c(2,1))
plot(BC.GlobalTemp_ts, type = 'o', ylab = 'Anomaly in Land Temperature', xlab = 'Year',
     main = "Transformed Time series plot of Global Land Temperature Anomalies in Degrees Celsius",
     col = "Blue", pch = 10)
plot(GlobalTemp_ts, type = 'o', ylab = 'Anomaly in Land Temperature', xlab = 'Year',
     main = "Time series plot of Global Land Temperature Anomalies in Degrees Celsius",
     col = "maroon", pch = 15)


# QQ line
qqnorm(BC.GlobalTemp_ts, ylab="Box-Cox GlobalTemp_ts", xlab="Normal Scores",
       col= 'darkcyan',
       main="QQ Plot of Transformed Global Temperature Time Series")
qqline(BC.GlobalTemp_ts, col = 'darkred')

# Shapiro Wilk Test
shapiro.test(BC.GlobalTemp_ts)

# Stationarity test of transformed series
stationarity_tests(BC.GlobalTemp_ts)


# Doing first Difference
diff.GlobalTemp_ts = diff(GlobalTemp_ts)

# Plotting the differenced series
plot(diff.GlobalTemp_ts, type='o', pch=10, ylab='Anomaly in Land Temperature',col="coral3", 
     xlab='Year', main="Time Series plot of differenced Series")

# Unit-root test of Differenced series
stationarity_tests(diff.GlobalTemp_ts)

# After performing first Differencing we can see that the series has become stationary
# and the mean level is constant. So, we won't do further on differencing in the series.

# ACF and PACF plot
par(mfrow=c(2,1))
acf(diff.GlobalTemp_ts, main ="ACF plot of the first differenced Anomaly in Land Temperature series.")
pacf(diff.GlobalTemp_ts, main ="PACF plot of the first differenced Anomaly in Land Temperature series.")


graphics.off()

# Specifying orders on the basis of ACF and PACF
# Set of possible ARIMA models: {ARIMA(1,1,1),ARIMA(1,1,2)}

# EACF Plot
eacf(diff.GlobalTemp_ts)

# The first zero not interrupted by X is at 0,2.
# Specifying orders on the basis of EACF 
# Set of possible ARIMA models: {ARIMA(0,1,2), ARIMA(0,1,3), ARIMA(1,1,2), ARIMA(1,1,3)}

# BIC table
res = armasubsets(y=diff.GlobalTemp_ts, nar=6, nma=6, y.name='p', ar.method='ols')
plot(res)

# Specifying orders on the basis of BIC table
# Set of possible ARIMA models: {ARIMA(2,1,5), ARIMA(2,1,1), ARIMA(2,1,0)}

# All possible models
# {ARIMA(1,1,1),ARIMA(0,1,2), ARIMA(0,1,3), ARIMA(1,1,2), ARIMA(1,1,3) } 
# {ARIMA(2,1,5), ARIMA(2,1,1), ARIMA(2,1,0)}

# Coefficient Estimation
orders <- list(c(1, 1, 1), c(0, 1, 2), c(0, 1, 3), c(1, 1, 2), c(1, 1, 3), c(2, 1, 5), c(2, 1, 1), c(2,1,0))
methods <- c("CSS", "ML","CSS-ML")
model_results <- fit_arima_models(GlobalTemp_ts, orders, methods)
model_results

sort.score(AIC(model_111_ml,model_012_ml,model_013_ml,model_112_ml,model_113_ml,
               model_215_ml,model_211_ml,model_210_ml), score = "aic")
sort.score(BIC(model_111_ml,model_012_ml,model_013_ml,model_112_ml,model_113_ml,
               model_215_ml,model_211_ml,model_210_ml), score = "bic" )

# Error measures
Smodel_111_css <- accuracy(model_111_css)[1:7]
Smodel_012_css <- accuracy(model_012_css)[1:7]
Smodel_013_css <- accuracy(model_013_css)[1:7]
Smodel_112_css <- accuracy(model_112_css)[1:7]
Smodel_113_css <- accuracy(model_113_css)[1:7]
Smodel_215_css <- accuracy(model_215_css)[1:7]
Smodel_211_css <- accuracy(model_211_css)[1:7]
Smodel_210_css <- accuracy(model_210_css)[1:7]
df.Smodels <- data.frame(
  rbind(Smodel_111_css,Smodel_012_css,Smodel_013_css,
        Smodel_112_css,Smodel_113_css,Smodel_215_css,Smodel_211_css,Smodel_210_css)
)
colnames(df.Smodels) <- c("ME", "RMSE", "MAE", "MPE", "MAPE", 
                          "MASE", "ACF1")
rownames(df.Smodels) <- c("ARIMA(1,1,1)", "ARIMA(0,1,2)", "ARIMA(0,1,3)", 
                          "ARIMA(1,1,2)", "ARIMA(1,1,3)", "ARIMA(2,1,5)","ARIMA(2,1,1)","ARIMA(2,1,0)")
round(df.Smodels,  digits = 3)

# Over parameterising ARIMA(1,1,3) and ARIMA (2,1,0)
# For ARIMA (1,1,3) we get ARIMA(2,1,3) and ARIMA (1,1,4)
# For ARIMA (2,1,0) we get ARIMA(3,1,0) and ARIMA(2,1,1)

orders <- list(c(2,1,3),c(1,1,4),c(3,1,0),c(2,1,1))
over_parameterised_model <- fit_arima_models(GlobalTemp_ts, orders, methods)
over_parameterised_model



# Model name defining for AIC, BIC and error measures

model_111_css = Arima(GlobalTemp_ts,order=c(1,1,1),method='CSS')
model_111_ml = Arima(GlobalTemp_ts,order=c(1,1,1),method='ML')

model_013_css = Arima(GlobalTemp_ts,order=c(0,1,3),method='CSS')
model_013_ml = Arima(GlobalTemp_ts,order=c(0,1,3),method='ML')

model_012_css = Arima(GlobalTemp_ts,order=c(0,1,2),method='CSS')
model_012_ml = Arima(GlobalTemp_ts,order=c(0,1,2),method='ML')

model_112_css = Arima(GlobalTemp_ts,order=c(1,1,2),method='CSS')
model_112_ml = Arima(GlobalTemp_ts,order=c(1,1,2),method='ML')

model_113_css = Arima(GlobalTemp_ts,order=c(1,1,3),method='CSS')
model_113_ml = Arima(GlobalTemp_ts,order=c(1,1,3),method='ML')

model_215_css = Arima(GlobalTemp_ts,order=c(2,1,5),method='CSS')
model_215_ml = Arima(GlobalTemp_ts,order=c(2,1,5),method='ML')

model_211_css = Arima(GlobalTemp_ts,order=c(2,1,1),method='CSS')
model_211_ml = Arima(GlobalTemp_ts,order=c(2,1,1),method='ML')

model_210_css = Arima(GlobalTemp_ts,order=c(2,1,0),method='CSS')
model_210_ml = Arima(GlobalTemp_ts,order=c(2,1,0),method='ML')

