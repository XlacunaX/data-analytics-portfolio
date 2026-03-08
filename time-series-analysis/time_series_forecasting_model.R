# To clean all the R memory
rm(list=ls())

# Loading time series package in R
library(TSA)

# setting up the working directory
setwd("C:/Users/shamb/OneDrive/Desktop/Time Series Analysis/Assignment 1")

# Reading the data file of Share Market Trader's Investment Portfolio
ShareMarket <- read.csv("assignment1Data2024.csv")

# View the loaded file
ShareMarket
head(ShareMarket)
class(ShareMarket)
plot(ShareMarket, type='o', ylab= 'Share Market Investment')

# Convert dataset ShareMarket to a time series data
ShareMarketTS <- ts((ShareMarket$x), frequency = 5)
ShareMarketTS

# View the TS data file
class(ShareMarketTS)
plot(ShareMarketTS, type='o', ylab= 'Investment return amount', main= "Time series plot of share market trader investment")
summary(ShareMarketTS)

# Creating first lag
orig = ShareMarketTS 
l = zlag(ShareMarketTS) 
index = 2:length(orig)
cor(orig[index],l[index]) 

# Creating second lag
l2 = zlag(zlag(ShareMarketTS))
index = 3:length(l2)
cor(orig[index],l2[index]) 

# ACF plot of lags
acf(ShareMarketTS, lag.max = 50)

# Extracting coefficients and intercept
coefficients <- coef(linearmodel)
intercept <- coefficients[1]
coefficients

# Fitting the linear model
t <- time(ShareMarketTS)
dataFreq <- frequency(ShareMarketTS)
linearmodel = lm(ShareMarketTS ~ t) 
summary(linearmodel)

fitted.linearmodel<- fitted(linearmodel)
plot(ShareMarketTS,type='o',ylab='Return_Amount', xlab='Day',main= 'Linear model fitted to Share Market series', ylim = c(-49.167,214.611))
abline(linearmodel)

# Residual Analysis of linearmodel
res.linearmodel = rstudent(linearmodel)
par(mfrow=c(3,3))
plot(y = res.linearmodel, x = as.vector(time(ShareMarketTS)),xlab = 'Day', ylab='Standardized Residuals',type='l',main = "Standardised residuals from linear model.")
hist(res.linearmodel, main = "Histogram of standardised residuals from linear model.")
qqnorm(y=res.linearmodel, main = "QQ plot of standardised residuals from linear model.")
qqline(y=res.linearmodel, col = 2, lwd = 1, lty = 2)
shapiro.test(res.linearmodel)
acf(res.linearmodel, main = "ACF of standardized residuals from linear model.")
pacf(res.linearmodel, main = "PACF of standardized residuals from linear model.")
graphics.off()


# Fitting the quadratic model
t = time(ShareMarketTS)
t2 = t^2
quadmodel = lm(ShareMarketTS~ t + t2)
summary(quadmodel)

fitted.quadmodel <- fitted(quadmodel)
plot(ts(fitted.quadmodel), ylim = c(min(c(fitted(quadmodel), as.vector(ShareMarketTS))), max(c(fitted(quadmodel),
    as.vector(ShareMarketTS)))), ylab='y' , main = "Fitted quadratic curve to Share Market series", type="l",lty=2,col="red")
lines(as.vector(ShareMarketTS),type="o")

# Residual Analysis
res.quadmodel = rstudent(quadmodel)

plot(y = res.quadmodel, x = as.vector(time(ShareMarketTS)),xlab = 'Time', 
     ylab='Standardized Residuals',type='l',main = "Standardised residuals from quadratic model.")
hist(res.quadmodel,xlab='Standardized Residuals', main = "Histogram of standardised residuals from quadratic model.")
qqnorm(y=res.quadmodel, main = "QQ plot of standardised residuals from quadratic model.")
qqline(y=res.quadmodel, col = 2, lwd = 1, lty = 2)
shapiro.test(res.quadmodel)
par(mfrow=c(2,1))
acf(res.quadmodel, main = "ACF of standardized residuals from quadratic model.")
pacf(res.quadmodel, main = "PACF of standardized residuals from quadratic model.")

# Fitting the Seasonal model
day.= season(ShareMarketTS)
dataFreq <- frequency(ShareMarketTS) 
seasonalmodel=lm(ShareMarketTS~day.-1)
summary(seasonalmodel)


fitted.seasonalmodel <- fitted(seasonalmodel)
plot(ts(fitted(seasonalmodel)), ylab='y', main = "Fitted seaonal model to Share Market series.",
     ylim = c(min(c(fitted(seasonalmodel), as.vector(ShareMarketTS))) ,
              max(c(fitted(seasonalmodel), as.vector(ShareMarketTS)))
     ), col = "red" )
lines(as.vector(ShareMarketTS),type="o")

# Residual Analysis
res.seasonalmodel = rstudent(seasonalmodel)
plot(y = res.seasonalmodel, x = as.vector(time(ShareMarketTS)),xlab = 'Time', 
     ylab='Standardized Residuals',type='l',main = "Standardised residuals from seasonal model.")
points(y=res.seasonalmodel,x=time(ShareMarketTS), pch=as.vector(season(ShareMarketTS)))
hist(res.seasonalmodel,xlab='Standardized Residuals', main = "Histogram of standardised residuals from seasonal model.")
qqnorm(y=res.seasonalmodel, main = "QQ plot of standardised residuals from seasonal model.")
qqline(y=res.seasonalmodel, col = 2, lwd = 1, lty = 2)
shapiro.test(res.seasonalmodel)
par(mfrow=c(2,1))
acf(res.seasonalmodel, main = "ACF of standardized residuals from seasonal model.")
pacf(res.seasonalmodel, main = "PACF of standardized residuals from seasonal model.")
graphics.off()

# Fitting quadratic + seasonal model
day. <- season(ShareMarketTS)
t <- time(ShareMarketTS)
t2 <- t^2
modelqs <- lm(ShareMarketTS ~ day. + t + t2 -1) 
summary(modelqs)
fitted.modelqs<- fitted(modelqs)
plot(ts(fitted(modelqs)), ylim = c(min(c(fitted(modelqs), as.vector(ShareMarketTS))), 
                                   max(c(fitted(modelqs),as.vector(ShareMarketTS)))),
     ylab='y' , main = "Fitted seasonal plus quadratic curve to Share Market series", type="l",lty=2,col="red")
lines(as.vector(ShareMarketTS),type="o")

# Residual Analysis
res.modelqs = rstudent(modelqs)
plot(y = res.modelqs, x = as.vector(time(ShareMarketTS)),xlab = 'Time', 
     ylab='Standardized Residuals',type='l',main = "Standardised residuals from quadratic plus seasonal model.")
points(y=res.modelqs,x=time(ShareMarketTS), pch=as.vector(season(ShareMarketTS)))
hist(res.modelqs,xlab='Standardized Residuals', main = "Histogram of standardised residuals from quadratic plus seasonal model.")
qqnorm(y=res.modelqs, main = "QQ plot of standardised residuals from quadratic plus seasonal model.")
qqline(y=res.modelqs, col = 2, lwd = 1, lty = 2)
shapiro.test(res.modelqs)
par(mfrow=c(2,1))
acf(res.modelqs, main = "ACF of standardized residuals.",lag.max = 60)
pacf(res.modelqs, main = "PACF of standardized residuals.")
graphics.off()


# Fitting the cosine/harmonic model
har.=harmonic(ShareMarketTS, 1)
data <- data.frame(ShareMarketTS,har.)
harmonicmodel = lm(ShareMarketTS ~ cos.2.pi.t. + sin.2.pi.t. , data = data)
summary(harmonicmodel)

fitted.harmonicmodel <- fitted(harmonicmodel)
plot(ts(fitted(harmonicmodel)), ylim = c(min(c(fitted.harmonicmodel),as.vector(ShareMarketTS)),
                                         max(c(fitted.harmonicmodel),as.vector(ShareMarketTS))),
     ylab='y' , main = "Fitted cosine curve on Share Market series", type="l",lty=2,col="red")
lines(as.vector(ShareMarketTS),type="o")

# Residual Analysis
res.harmonicmodel = rstudent(harmonicmodel)
plot(y = res.harmonicmodel, x = as.vector(time(ShareMarketTS)),xlab = 'Time', ylab='Standardized Residuals',type='l'
     ,main = "Standardised residuals from harmonic model.")
points(y=res.harmonicmodel,x=time(ShareMarketTS.ts), pch=as.vector(season(ShareMarketTS)))
hist(res.harmonicmodel,xlab='Standardized Residuals', main = "Histogram of standardised residuals from harmonic model.")
qqnorm(y=res.harmonicmodel, main = "QQ plot of standardised residuals from harmonic model.")
qqline(y=res.harmonicmodel, col = 2, lwd = 1, lty = 2)
shapiro.test(res.harmonicmodel)
par(mfrow=c(2,1))
acf(res.harmonicmodel, main = "ACF of standardized residuals from harmonic model.")
pacf(res.harmonicmodel, main = "PACF of standardized residuals from harmonic model.")



# FORECASTING FROM THE BEST FIT MODEL
# Next five trading days forecast
h <- 5 
lastTimePoint <- t[length(t)]
aheadTimes <- data.frame(t = seq(lastTimePoint+(1/dataFreq), lastTimePoint+h*(1/dataFreq), 1/dataFreq),
                         t2 =  seq(lastTimePoint+(1/dataFreq), lastTimePoint+h*(1/dataFreq), 1/dataFreq)^2) 

frcquadmodel <- predict(quadmodel, newdata = aheadTimes, interval = "prediction")

plot(ShareMarketTS, xlim= c(t[1],aheadTimes$t[nrow(aheadTimes)]), ylim = c(-150,300), ylab = "Share Market series", xlab="days",
     main = "Forecasts from the quadratic model fitted to the  Share Market series.")
lines(ts(fitted.quadmodel,start = t[1],frequency = dataFreq)) 
lines(ts(as.vector(frcquadmodel[,3]), start = aheadTimes$t[1],frequency = dataFreq), col="dark green", type="l")
lines(ts(as.vector(frcquadmodel[,1]), start = aheadTimes$t[1],frequency = dataFreq), col="maroon", type="l")
lines(ts(as.vector(frcquadmodel[,2]), start = aheadTimes$t[1],frequency = dataFreq), col="dark green", type="l")
legend("topleft", lty=1, pch=1, col=c("black","dark green","maroon"), 
       c("Data","5% forecast limits", "Forecasts"))


