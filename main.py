import pandas as pd
from db_utils import RDSDatabaseConnector
from datatransformation import DataTransform
from inspectdata import DataFrameInfo
from plotter import Plotter
from dataframetransformation import DataFrameTransform

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
    """

    df = load_data()

    #initial info about data
    info = DataFrameInfo(df)
    types = info.describe_types()
    print("Initial Data Types:\n", types)
    total_nulls = info.count_nulls()
    print("Initial Null Values:\n", total_nulls)

    transformer = DataTransform(df)
    
    #columns for transformation
    columns_to_transform_float_to_int = ['mths_since_last_record', 'mths_since_last_delinq', 'collections_12_mths_ex_med', 'mths_since_last_major_derog']
    columns_to_transform_mixed_obj_to_int = ['term', 'employment_length']
    columns_to_transform_date_object_to_datetime = ['issue_date', 'earliest_credit_line', 'last_payment_date', 'next_payment_date', 'last_credit_pull_date']
    columns_to_transform_to_categorical = ['grade', 'sub_grade', 'home_ownership', 'verification_status', 'loan_status', 'payment_plan','purpose','policy_code', 'application_type']

    #apply transformations
    transformer.convert_float_to_int(columns_to_transform_float_to_int)
    transformer.convert_mixed_obj_to_int(columns_to_transform_mixed_obj_to_int)
    transformer.convert_date_object_to_datetime(columns_to_transform_date_object_to_datetime)
    transformer.convert_to_categorical(columns_to_transform_to_categorical)

    #info following transformations
    types = info.describe_types()
    print("Transformed Data Types:\n", types)
    total_nulls = info.count_nulls()
    print("Transformed Null Values:\n", total_nulls)
    
    #save the transformed DataFrame to a CSV file used in all below
    df.to_csv('loan_payments_transformed.csv', index=False)
    print("Transformed DataFrame saved as 'loan_payments_transformed.csv'.")

    #varible for CSV file to use for below 
    df = pd.read_csv('loan_payments_transformed.csv')

    #inspect and analyse transformed data
    info = DataFrameInfo(df)

    stats = info.describe_stats()
    print("Descriptive Statistics:\n", stats)

    distinct_vals = info.count_distinct_values()
    print("Distinct Values:\n", distinct_vals)

    print("DataFrame Shape:", df.shape)

    plotter = Plotter(df)
    dftransform = DataFrameTransform(df)

    #deal with null values
    plotter.plot_null_values()
    dftransform.drop_nulls_over_threshold()
    dftransform.impute_missing_values()

    #plot null values after transformation
    plotter.plot_null_values()
    total_nulls = info.count_nulls()
    print("Null Values:\n", total_nulls)

    #deal with skewness
    for col in df.select_dtypes(include=['number']).columns:
        plotter.plot_distribution(col)

    skewed_columns = dftransform.identify_skewed_columns(skew_threshold=1)
    print("Skewed columns:\n", skewed_columns)
    dftransform.transform_skewed_columns()

    #plot skewness after transformation
    for col in df.select_dtypes(include=['number']).columns:
        plotter.plot_distribution(col)

    #deal with outliers
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    for column in numeric_columns:
        plotter.plot_boxplot(column)

    for col in df.select_dtypes(include=['number']).columns:
        dftransform.remove_outliers(col)

    #visualise data after removing outliers
    for col in df.select_dtypes(include=['number']).columns:
        plotter.plot_boxplot(col)

    #deal with high correlation
    plotter.plot_correlation_matrix()
    df_reduced, removed_columns = dftransform.remove_highly_correlated_columns(threshold=0.9)
    print(f"Removed columns: {removed_columns}")

    #visualise data after removing columns of high correlation
    plotter.data = df_reduced
    plotter.plot_correlation_matrix()

    #save the transformed DataFrame
    df_reduced.to_csv('loan_payments_transformed.csv', index=False)
    print("DataFrame saved as 'loan_payments_transformed.csv'.")

if __name__ == "__main__":
    main()

