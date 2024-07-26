import pandas as pd
from db_utils import RDSDatabaseConnector
from datatransformation import DataTransform
from inspectdata import DataFrameInfo
from plotter import Plotter
from dataframetransformation import DataFrameTransform
from visualisations import Visualisations

def load_data():
    """
    Loads data from an RDS database using credentials from RDSDatabaseConnector.

    Returns:
        pandas.DataFrame: DataFrame containing loan payments data.
    """
    credentials = RDSDatabaseConnector.load_credentials()
    connector = RDSDatabaseConnector(credentials)
    df = connector.extract_loan_payments()
    return df


def main():

    """

    Main function to process loan payments data:
    - Transform data types
    - Describe data statistics
    - Handle missing values
    - Handle outliers
    - Remove highly correlated columns
    - Visualise and save results
    - Produce business intelligence data for company

    """

    df = load_data()

    #use csv file as a copy
    df.to_csv('loan_payments_transformed.csv', index=False)
    print("Transformed DataFrame saved as 'loan_payments_transformed.csv'.")
    df = pd.read_csv('loan_payments_transformed.csv')
    
    info = DataFrameInfo(df)
    plotter = Plotter(df)
    transformer = DataTransform(df)
    dftransform = DataFrameTransform(df)
    analysis = Visualisations(df)
    
    #initial info about data
    types = info.describe_types()
    print("Initial Data Types:\n", types)
    total_nulls = info.count_nulls()
    print("Initial Null Values:\n", total_nulls)
    plotter.plot_null_values()
    info.percentage_of_zeros()    
    stats = info.describe_stats()
    print("Descriptive Statistics:\n", stats)
    distinct_vals = info.count_distinct_values()
    print("Distinct Values:\n", distinct_vals)
    print("DataFrame Shape:", df.shape)

    #deal with null values
    dftransform.drop_nulls_over_threshold()
    dftransform.drop_rows_in_datetime("last_payment_date")
    dftransform.drop_rows_in_datetime("last_credit_pull_date")
    transformer.apply_transformations()
    dftransform.impute_missing_values() 

    #info following transformations
    types = info.describe_types()
    print("Transformed Data Types:\n", types)
    total_nulls = info.count_nulls()
    print("Transformed Null Values:\n", total_nulls)
    plotter.plot_null_values()

    #deal with outliers, fix
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    for column in numeric_columns:
        plotter.plot_scatter_plot(column)
    for col in df.select_dtypes(include=['number']).columns:
        dftransform.remove_outliers(col)

    #deal with skewness, fix
    for col in df.select_dtypes(include=['number']).columns:
        plotter.plot_distribution(col)
    skewed_columns = dftransform.identify_skewed_columns(skew_threshold=1)
    print("Skewed columns:\n", skewed_columns)
    dftransform.transform_skewed_columns()
    print("Skewed columns:\n", skewed_columns)

    #plot high correlation, decided not to remove columns as all relevant
    plotter.plot_correlation_matrix()

    analysis.loan_recovery_graphs()
    analysis.losses_calc()
    analysis.display_charged_off_loans_info()
    analysis.projected_loss_calc()
    analysis.visualise_projected_loss() #simplified following a conversation with AiCore due to deadlines

    analysis.at_risk_customers_calculation() #check calculation
    analysis.at_risk_customers_visualisation() #final part incomplete, on to do list

    analysis.create_subset()
    analysis.analyse_grade()
    analysis.analyse_purpose()
    analysis.analyse_home_ownership()

if __name__ == "__main__":
    main()

