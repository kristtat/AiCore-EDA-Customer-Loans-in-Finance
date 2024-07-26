# AiCore-EDA-Customer-Loans-in-Finance

This project is an Exploratory Data Analysis (EDA) exercise developed as part of the AiCore Data Analytics bootcamp.

# Description of project

The project involves analysing customer loan data from the finance sector using Python. It explores various statistical measures, data transformations and visualisations to gain insights into the dataset.

## Aim:

The aim is to perform exploratory data analysis on the loan portfolio, using various statistical and data visualisation techniques to uncover patterns, relationships, and anomalies in the loan data to enable the business to make informed decisions about loan approvals, pricing, and risk management.

# Learning points

- Pandas Series Objects: I learned about Pandas Series objects and how they behave.
- Heatmaps: I learned about the use of heatmaps to enable quick identification of patterns or anomalies in data.
- Numeric vs non numeric data visualisation: I learned about different visualisations for different data types.
- Combining columns vs. separating them: I played around with different options for visualisations to see if I should represent data from all columns together or separately.
- Iterative approach: Tried to separate methods as much as possible to enable reusability of code.
- Skewness: Transforming data to correct skewness took the longest, good learning point for next time. 
- Pydoc + README: I left these last and it took me nearly a whole day to write these up, definitely will do these as I go next time. 
- Zeros: Dealt with null values but not with zeros, added this method.
- Ordering of methods called: Moved methods around to ensure data as robust as possible.
- Removal of nulls: Initially converted data first before removing nulls but this caused issues down the line, changed order.
- Split imputation methods: Although one method worked fine initially, I split these into numeric and non numeric to deal with bugs after changes in remaining code.
- High correlation: Ended up not implemeting methods I wrote to deal with high correlation as I needed them for calculations or they were valid data (e.g. total funded and investor funded, and ID and Member ID).
  
# Future Learning

- Handling of numeric and non-numeric: I struggled with converting values like 10+ into numeric. Would want to understand how relevant the 10+ is and can it be replaced with 11 for example, and to understand how I can convert these into integers. 
- Imputation Strategy: I will read up more about how to choose between median and mean imputation. For this project I selected to go with mean if (mean-median) within 10% of mean as I read that this was recommended.
- Dealing with Highly Correlated Data: I will explore more on managing highly correlated categorical data.
- Optimal Chart Sizes: I will go away and learn more about ideal chart sizes for different visualisations to enhance readability.

# Installation instructions

Install all named packages.

# Use instructions

The programme runs by running main.py.

# File structure of the project

credentials: Contains credentials.
.gitignore: Specifies files and directories to be ignored by GitHub.
db_utils: Module containing methods to extract data from the RDS database.
inspectdata: Module containing methods to inspect data in the Pandas DataFrame.
plotter: Module containing methods for plotting functionalities.
datatransformation: Module containing methods for data transformation operations.
dataframetransformation: Module for DataFrame-specific transformations.
visualisations: Module for calculating and visualising business intelligence data relevant to company. 
main: Main module.

### To Do
- Add error handling.
- Resolve issues with the outlier removal method.
- Resolve issue with over 100% recovered investor percentage - outlier related?
- Resolve issues with at_risk_customers_calculation. 
- Complete Milestone 4 task 3.
- Complete Milestone 4 task 4. 