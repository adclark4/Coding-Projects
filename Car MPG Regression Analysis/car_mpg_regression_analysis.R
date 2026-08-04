############################################################
# Project: Car MPG Regression Analysis
# File: car_mpg_regression_analysis.R
# Author: Anthony "AJ" Clark
#
# Description:
# This project explores the built-in 'mtcars' dataset in R
# and builds linear regression models to predict fuel
# efficiency (miles per gallon - mpg) from car features
# such as horsepower, weight, and cylinders.
#
# Skills Demonstrated:
# - Data exploration and visualization
# - Simple and multiple linear regression modeling
# - Model interpretation (coefficients, R^2, significance)
# - Assumption checking with diagnostic plots
# - Communication of insights
############################################################

# Load the built-in dataset into the R environment
data(mtcars)

# Preview the dataset to understand its structure (first 6 rows)
head(mtcars)

# Display structure of the dataset: variable names, types, dimensions
str(mtcars)

# Generate summary statistics for each variable
# Includes mean, median, min, max, and quartiles
summary(mtcars)

# Build a simple linear regression model to predict mpg
# using horsepower (hp) as the single predictor
model1 <- lm(mtcars$mpg ~ mtcars$hp)

# Display regression summary:
# - Coefficients: intercept and slope for horsepower
# - p-value: significance of horsepower as a predictor
# - R-squared: proportion of variance explained
# - Residual Std. Error: average prediction error
summary(model1)

# Build a multiple linear regression model to predict mpg
# using horsepower (hp), weight (wt), and number of cylinders (cyl)
model2 <- lm(mtcars$mpg ~ mtcars$hp + mtcars$wt + mtcars$cyl)

# Display regression summary:
# - Coefficients: intercept and slopes for each predictor
# - p-values: statistical significance of predictors
# - Adjusted R-squared: model fit adjusted for number of predictors
# - Residual Std. Error: typical size of prediction error
summary(model2)

# Compare simple regression model (model1: mpg ~ hp) with the
# multiple regression model (model2) using ANOVA
# Tests whether adding predictors significantly improves model fit
anova(model1, model2)

