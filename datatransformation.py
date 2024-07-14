import pandas as pd

class DataTransform:

    """
    A class containing methods to transform columns in a Pandas DataFrame.

    Methods:
        __init__(self, df):
            Initializes the DataTransform object with a given DataFrame.

        convert_float_to_int(self, columns):
            Converts specified columns to integer type after filling NaN values with 0.

        convert_mixed_obj_to_int(self, columns):
            Converts specified columns containing mixed data types to integer after coercing to numeric type.
        
        convert_date_object_to_datetime(self, columns):
            Converts specified columns containing date objects to datetime format with specified format.

        convert_to_categorical(self, columns):
            Converts specified columns to categorical type.

    """

    def __init__(self, df):

        """

        Initialises the DataFrameInfo object with a given DataFrame.

        Parameters:
            df (pandas.DataFrame): The DataFrame to inspect.

        """

        self.df = df
    
    def convert_float_to_int(self, columns):

        """

        Converts columns to integer type after filling NaN values with 0.

        Parameters:
            columns (list): List of column names to convert.

        Returns:
            pandas.DataFrame: DataFrame with specified columns converted to integer type.

        """

        for col in columns:
            self.df[col] = self.df[col].fillna(0).astype(int)
        print("All relevant columns converted to integer type.")
        return self.df

    def convert_mixed_obj_to_int(self, columns):

        """
        
        Converts specified columns containing mixed data types to integer after coercing to numeric type and fills NaNs as 0.

        Parameters:
            columns (list): List of column names to convert.

        Returns:
            pandas.DataFrame: DataFrame with specified columns converted to integer type.

        
        """

        for col in columns:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0).astype(int)
        print("All relevant columns converted to integer type.")
        return self.df

    def convert_date_object_to_datetime(self, columns):

        """
        
        Converts specified columns containing date objects to datetime format.

        Parameters:
            columns (list): List of column names to convert.

        Returns:
            pandas.DataFrame: DataFrame with specified columns converted to datetime format.
        
        """
        for col in columns:
            self.df[col] = pd.to_datetime(self.df[col], format='%b-%Y')
        print("All relevant columns converted to datetime type.")
        return self.df

    def convert_to_categorical(self, columns):

        """
        Converts specified columns to categorical type.

        Parameters:
            columns (list): List of column names to convert.

        Returns:
            pandas.DataFrame: DataFrame with specified columns converted to categorical type.

        
        """
        for col in columns:
            self.df[col] = self.df[col].astype('category')
        print("All relevant columns converted to categorical type.")
        return self.df


 