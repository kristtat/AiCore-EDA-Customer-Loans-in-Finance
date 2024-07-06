import pandas as pd
import psycopg2
import yaml
from sqlalchemy import create_engine


class RDSDatabaseConnector:

    """
    A class to contain methods to extract data from the RDS database.

    Methods:
        __init__(self, credentials): 
            Initialises the RDSDatabaseConnector with given credentials.

        load_credentials(): 
            Loads the credentials.yaml file and returns the data dictionary contained within.

        connect_to_database(self): 
            Connects to the RDS database using the provided credentials and returns the connection object.

        create_engine(self): 
            Initialises a SQLAlchemy engine from the credentials provided to class. 
            This engine object together with the Pandas library allows extraction of data from the database.

        extract_loan_payments(self): 
            Extracts data from the RDS database and returns it as a Pandas DataFrame. 
            The data is stored in a table called loan_payments.

        save_data(self, dataframe, filename): 
            Saves the data as a CSV file to local machine. 

        load_data(self, filename): 
            Loads data from CSV file into a Pandas DataFrame.
    """
    
    def __init__(self, credentials):
        """
        Initialises the RDSDatabaseConnector with given credentials.

        Parameters:
            credentials(dict): A dictionary containing database connection details.
        
        """
        self.credentials = credentials
    
    @staticmethod
    def _load_credentials():
        """
        Loads the credentials from 'credentials.yaml' file.

        Returns:
            dict: A dictionary containing the credentials.
        """
        with open('credentials.yaml', 'r') as f:
            credentials = yaml.safe_load(f)
        return credentials

    def connect_to_database(self):
        """
        Connects to the RDS database using the provided credentials.

        Returns:
            A connection object to the RDS database.
        """
        conn = psycopg2.connect(
            host=self.credentials['RDS_HOST'],
            password=self.credentials['RDS_PASSWORD'],
            user=self.credentials['RDS_USER'],
            database=self.credentials['RDS_DATABASE'],
            port=self.credentials['RDS_PORT']            
        )
        print("Connected to database successfully!")
        return conn

    def create_engine(self):
        """
        Initialises a SQLAlchemy engine from the credentials provided to the class.

        Returns:
            An engine object for connecting to the database.
        """
        engine_str = f"postgresql+psycopg2://{self.credentials['RDS_USER']}:{self.credentials['RDS_PASSWORD']}@{self.credentials['RDS_HOST']}:{self.credentials['RDS_PORT']}/{self.credentials['RDS_DATABASE']}"
        engine = create_engine(engine_str)
        return engine

    def extract_loan_payments(self):
        """
        Extracts data from the RDS database and returns it as a Pandas DataFrame.
        The data is stored in a table called 'loan_payments'.

        Returns:
            A DataFrame containing the loan payments data.
        """
        conn = self.connect_to_database()
        query = "SELECT * FROM loan_payments;"
        df = pd.read_sql(query, conn)
        print("Successfully extracted loan payments data!")
        conn.close()
        return df
    
    def save_data(self, dataframe, filename):
        """
        Saves the data to a CSV file on local machine.

        Parameters:
            dataframe (pandas.DataFrame): The DataFrame to save.
            filename (str): The name of the file to save the data to.
        """
        dataframe.to_csv(filename, index=False)
    
    def load_data(self, filename):
        """
        Loads data from a CSV file into a Pandas DataFrame.

        Parameters:
            filename (str): The name of the file to load the data from.

        Returns:
            A DataFrame containing the loaded data.
        """
        df = pd.read_csv(filename)
        print(f"Loaded data from {filename} successfully!")
        return df


def main():
    """
    Main function to load credentials, connect to the database, extract loan payments data, 
    save the data to a CSV file, and then load the data from the CSV file.
    """
    credentials = RDSDatabaseConnector._load_credentials() 
    connector = RDSDatabaseConnector(credentials)
    connector.connect_to_database()
    df = connector.extract_loan_payments()
    connector.save_data(df, 'loan_payments_data.csv')
    loaded_df = connector.load_data('loan_payments_data.csv')
    print(loaded_df.head())

if __name__ == "__main__":
    main()