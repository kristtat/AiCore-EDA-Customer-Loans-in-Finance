import pandas as pd
import numpy as np
from scipy.stats import boxcox, skew


class DataFrameTransform:

    """
    A class containing methods to transform the Pandas DataFrame.

    Methods:
        __init__(self, credentials): 
            Initialises the DataFrameInfo object with a given DataFrame.

        drop_nulls_over_threshold(self, threshold=50): 
            Drops columns with null value of over 50%.

        impute_missing_values(self):
            Imputes null values with mean or median if column numeric and with mode if column non-numeric.

        identify_skewed_columns(self, skew_threshold=1):
            Identifies numerical columns with skewness outside threshold.

        transform_column(self, col, method):
            Transforms a specified column using a given method.

        find_best_transformation(self, col):
            Finds the best transformation for a column by comparing skewness after applying a transformation.

        apply_transformations(self, skewed_columns):
            Transforms skewed columns in the DataFrame using the best transformation method.

        remove_outliers(self, column):
            Removes outliers from a specified column in the DataFrame using the Interquartile Range method.

        identify_highly_correlated(self, threshold=0.9):
            Identifies pairs of numeric columns in the DataFrame that are highly correlated.

        remove_highly_correlated_columns(self, threshold=0.9):
            Removes columns from the DataFrame that are highly correlated with each other.

    """

    def __init__(self, df):

        """
        Initialises the DataFrameInfo object with a given DataFrame.

        Parameters:
            df (pandas.DataFrame): The DataFrame to inspect.
        """

        self.df = df

    def drop_nulls_over_threshold(self, threshold=50):

        """
        Drops columns with null value of over 50%.

        Parameters:
            threshold(int): Threshold for dropping. Default is 50%.
        """

        null_percentages = (self.df.isnull().sum() / len(self.df)) * 100
        columns_to_drop = null_percentages[null_percentages > threshold].index.tolist() #creates list of values and prints them
        print(f"Column(s) {columns_to_drop} exceed(s) threshold of 50% and has been dropped.")
        self.df.drop(columns=columns_to_drop, inplace=True)
        return self.df

    def impute_missing_values(self):

        """
        Imputes null values with mean or median if column numeric and with mode if column non-numeric.

        Returns:
            df (pandas.DataFrame): DataFrame with missing values imputed.

        """

        for col in self.df.columns:
            if self.df[col].isnull().any():
                if self.df[col].dtype in ['float64', 'int64']: #numeric columns, impute with mean or median
                    mean_value = self.df[col].mean()
                    median_value = self.df[col].median()
                    if abs(mean_value - median_value) / mean_value < 0.1:  #checks that difference between mean and median is within 10% of mean
                        self.df[col] = self.df[col].fillna(mean_value)
                    else:
                        self.df[col] = self.df[col].fillna(median_value)
                else:
                    self.df[col] = self.df[col].fillna(self.df[col].mode()[0]) #non-numeric columns, impute with mode
        return self.df

    def identify_skewed_columns(self, skew_threshold=1):

        """
        Identifies numerical columns with skewness outside threshold.

        Parameters:
            skew_threshold (float): Threshold for skewness. Default is 1.

        Returns:
            list: Column names with skewness < -skew_threshold or > skew_threshold.
        """

        skewed_columns = self.df.select_dtypes(include=['float64', 'int64']).apply(lambda x: x.skew())
        skewed_columns = skewed_columns[(skewed_columns < -skew_threshold) | (skewed_columns > skew_threshold)] #both -1 and +1
        return skewed_columns.index.tolist()


    def transform_column(self, col, method):

        """
        Transforms a specified column using a given method.

        Parameters:
            col (str): The name of the column to transform.
            method (str): The transformation method to apply. Must be 'log', 'sqrt', or 'boxcox'.

        Returns:
            pandas.Series: The transformed column.
            column: If column is non-numeric, returns column.

        """
        if self.df[col].dtype not in ['float64', 'int64']:
            print(f"Transformation {method} failed for column {col}: Non-numeric data type")
        return self.df[col]
    
        if method == 'log':
            return np.log1p(self.df[col])
        elif method == 'sqrt':
            return np.sqrt(self.df[col])
        elif method == 'boxcox':
            transformed_col = boxcox(self.df[col] + 1)[0] # +1 to avoid issues with zero or negative values
            return pd.Series(transformed_col, index=self.df.index)  # numpy array back to pandas Series
        else:
            raise ValueError("Invalid transformation method")

    def find_best_transformation(self, col):
        """
        Finds the best transformation for a column by comparing skewness after applying a transformation.

        Parameters:
            col (str): The name of the column to transform.

        Returns:
            str: The name of the best transformation method.
            pandas.Series: The transformed column using the best method.
        """

        transformations = ['log', 'sqrt', 'boxcox']
        best_method = None
        best_skew = np.inf
        best_transformed_col = self.df[col]

        for method in transformations:
            transformed_col = self.transform_column(col, method)
            skewness = transformed_col.skew()
            if abs(skewness) < abs(best_skew):
                best_skew = skewness
                best_method = method
                best_transformed_col = transformed_col

        return best_method, best_transformed_col


    def transform_skewed_columns(self, skew_threshold=1):
        """
    
        Transforms skewed columns in the DataFrame using the best transformation method.

        Parameters:
            skew_threshold (float): The skewness threshold to use for identifying skewed columns.

        Returns:
            pandas.DataFrame: The DataFrame with transformed columns.

        """
        
        skewed_columns = self.identify_skewed_columns(skew_threshold)

        for col in skewed_columns:
            best_method, best_transformed_col = self.find_best_transformation(col)
            self.df[col] = best_transformed_col
            print(f"Column '{col}' transformed using {best_method} method")

        return self.df

    def remove_outliers(self, column):

        """

        Removes outliers from a specified column in the DataFrame using the Interquartile Range method.

        Parameters:
            column (str): The name of the numeric column from which outliers will be removed. 

        Returns:
            pandas.DataFrame: A new DataFrame with outliers removed from the specified column. 
            The original DataFrame (`self.df`) is updated in place to exclude rows with outliers.

        """

        if pd.api.types.is_numeric_dtype(self.df[column]):
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            self.df = self.df[(self.df[column] >= lower_bound) & (self.df[column] <= upper_bound)]
        return self.df
        
    def identify_highly_correlated(self, threshold=0.9):

        """
        Identifies pairs of numeric columns in the DataFrame that are highly correlated.

        Parameters:
            threshold (float): Threshold above which columns considered highly correlated. Defaulted to 0.9.

        Returns:
            list: List of tuples, each tuple contains a pair of highly correlated column names.

        """
   
        numeric_data = self.df.select_dtypes(include=['float64', 'int64'])
        correlation_matrix = numeric_data.corr().abs()

        highly_correlated_pairs = []
        columns = correlation_matrix.columns

        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):
                if correlation_matrix.iloc[i, j] > threshold:
                    pair = (columns[i], columns[j])
                    highly_correlated_pairs.append(pair)

        return highly_correlated_pairs

    def remove_highly_correlated_columns(self, threshold=0.9):

        """
        
        Removes columns from the DataFrame that are highly correlated with each other.

        Parameters:
            threshold (float): Threshold above which columns considered highly correlated. Defaulted to 0.9.

        Returns:
            tuple: A tuple containing:
                pandas.DataFrame: The DataFrame with highly correlated columns removed.
                set: A set of column names that were removed due to high correlation.
    
        """

        correlated_columns = self.identify_highly_correlated(threshold)
        columns_to_remove = set()
        for col1, col2 in correlated_columns:
            columns_to_remove.add(col2)
        self.df.drop(columns=columns_to_remove, inplace=True)
        return self.df, columns_to_remove



