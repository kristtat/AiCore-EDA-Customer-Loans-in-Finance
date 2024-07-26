import pandas as pd

class DataFrameInfo:

    """
    A class containing methods to inspect data in the Pandas DataFrame.

    Methods:
        __init__(self, credentials): 
            Initialises the DataFrameInfo object with a given DataFrame.

        describe_types(self): 
            Returns data types of columns.

        describe_stats(self): 
            Returns mean, median and mode of each numerical column.

        count_distinct_values(self):
            Returns distinct values of each categorical column.

        count_nulls(self):
            Counts null values in each column. 

        percentage_of_zeros(self, column):
            Calculates the percentage of zeros in the specified column.
    """

    def __init__(self, df):
        
        """
        Initialises the DataFrameInfo object with a given DataFrame.

        Parameters:
            df (pandas.DataFrame): The DataFrame to inspect.
        """

        self.df = df

    def describe_types(self):

        """
        Returns the data types of all columns in the DataFrame.

        Returns:
            pandas.Series: A Series containing the data types of each column.
        """

        return self.df.dtypes
        
    def describe_stats(self):

        """
        Returns the mean, median, and mode of each numerical column in the DataFrame.

        Returns:
            dict: A dictionary where keys are column names and values are dictionaries containing mean, median, and mode statistics.
        """

        stats = {}
        for col in self.df.select_dtypes(include='number').columns:
            stats[col] = {
                'mean': self.df[col].mean() if self.df[col].dtype in ['float64', 'int64'] else None,
                'median': self.df[col].median() if self.df[col].dtype in ['float64', 'int64'] else None,
                'mode': self.df[col].mode()[0] if not self.df[col].mode().empty else None,
            
            }
        return stats

    def count_distinct_values(self):

        """
        Returns the distinct values of each categorical column in the DataFrame.

        Returns:
            dict: A dictionary where keys are categorical column names and values are arrays containing unique values.
        """

        categorical_columns = self.df.select_dtypes(include='category').columns
        distinct_counts = {}
        for col in categorical_columns:
            distinct_counts[col] = self.df[col].unique()
        return distinct_counts

    def count_nulls(self):

        """
        Counts null values in each column of the DataFrame.

        Returns:
            pandas.DataFrame: A DataFrame showing the count and percentage of null values for each column.
        """

        null_counts = self.df.isnull().sum()
        total_counts = len(self.df)
        null_percentage = (null_counts / total_counts) * 100
        result = pd.DataFrame({'Null Count': null_counts, 'Null Percentage': null_percentage})
        return result

    def percentage_of_zeros(self):
        """
        Calculates the percentage of zeros in the specified column.

        Parameters:
            column (str): The name of the column to calculate the percentage of zeros for.

        Returns:
            float: The percentage of zeros in the specified column.
        """

        for col in self.df.columns:
            if pd.api.types.is_numeric_dtype(self.df[col]):
                total_count = len(self.df[col])
                if total_count == 0:
                    zero_percentage = 0.0
                else:
                    zero_count = (self.df[col] == 0).sum()
                    zero_percentage = (zero_count / total_count) * 100
                
                print(f"Percentage of zeros in column '{col}': {zero_percentage:.2f}%")