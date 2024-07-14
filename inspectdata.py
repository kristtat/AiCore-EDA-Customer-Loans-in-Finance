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
                'mean': self.df[col].mean(),
                'median': self.df[col].median(),
                'mode': self.df[col].mode()[0]
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