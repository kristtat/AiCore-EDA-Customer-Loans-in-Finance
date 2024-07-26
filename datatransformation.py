import pandas as pd

class DataTransform:

    """
    A class containing methods to transform columns in a Pandas DataFrame.

    Methods:
        __init__(self, df):
            Initialises the DataTransform object with a given DataFrame.

        convert_mixed_obj_to_int(self, columns):
            Converts specified columns containing mixed data types to integer after coercing to numeric type.
        
        convert_date_object_to_datetime(self, columns):
            Converts specified columns containing date objects to datetime format with specified format.

        convert_to_categorical(self, columns):
            Converts specified columns to categorical type.
            
        apply_transformations(self):
            Applies all transformations defined for the DataFrame.

    """

    def __init__(self, df):

        """

        Initialises the DataFrameInfo object with a given DataFrame.

        Parameters:
            df (pandas.DataFrame): The DataFrame to inspect.

        """

        self.df = df
    

    def convert_mixed_obj_to_int(self, columns):

        """
        Converts specified columns containing mixed data types to integer after extracting numeric part.
        Fills NaNs with 0.

        Parameters:
            columns (list): List of column names to convert.

        Returns:
            pandas.DataFrame: DataFrame with specified columns converted to integer type. 

        """
        
        for col in columns:
            try:
                self.df[col] = self.df[col].str.extract('(\d+)').fillna(0).astype(int)
                print(f"Converted column '{col}' to integer format.")
            except Exception as e:
                print(f"Error converting column '{col}': {e}")
        return self.df
        

    def convert_date_object_to_datetime(self, columns):

        """
        
        Converts specified columns containing date objects to datetime format.

        Parameters:
            columns (list): List of column names to convert.

        Returns:
            pandas.DataFrame: DataFrame with specified columns converted to datetime format.
        
        """
        date_format = "%b-%Y"
        for col in columns:
                self.df[col] = pd.to_datetime(self.df[col], format=date_format, errors='coerce')
                print(f"Converted column '{col}' to datetime format.")
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
            try:
                self.df[col] = self.df[col].astype('category')
                print(f"Converted column '{col}' to categorical format.")
            except Exception as e:
                print(f"Error converting column '{col}': {e}")
        return self.df
        

    def apply_transformations(self):

        """

        Applies all transformations defined for the DataFrame.


        """
       
        columns_to_transform_mixed_obj_to_int = ['term', 'employment_length']
        columns_to_transform_date_object_to_datetime = ['issue_date', 'earliest_credit_line', 'last_payment_date', 'last_credit_pull_date']
        columns_to_transform_to_categorical = ['grade', 'sub_grade', 'home_ownership', 'verification_status', 'loan_status', 'payment_plan','purpose','policy_code', 'application_type']

      
        self.convert_mixed_obj_to_int(columns_to_transform_mixed_obj_to_int)
        self.convert_date_object_to_datetime(columns_to_transform_date_object_to_datetime)
        self.convert_to_categorical(columns_to_transform_to_categorical)

        print("All transformations successfully completed.")
        return self.df
