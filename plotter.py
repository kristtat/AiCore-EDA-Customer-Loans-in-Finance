import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

class Plotter:

    """
    A class containing methods to plot data in the Pandas DataFrame.

    Methods:
        __init__(self, credentials): 
            Initialises the DataFrameInfo object with a given DataFrame.

        plot_null_values(self): 
            Generates a heatmap of null values.
            Generates a bar chart of null values if these exist and prints a message if no null values exist.

        plot_distribution(self, column):
            Generates a histogram of distribution of data in a column to inspect skewness. 

        plot_scatterplot(self, column):
            Generates a scatterplot of data in a column to inspect outliers.

        plot_correlation_matrix(self):
            Generates a heatmap to visualise the correlation of data.
    """

    def __init__(self, df):

        """
        Initialises the DataFrameInfo object with a given DataFrame.

        Parameters:
            df (pandas.DataFrame): The DataFrame to inspect.
        """

        self.df = df

    
    def plot_null_values(self):

        """
        Generates visualisations to show missing values in the DataFrame.

        Two plots:
        1. A heatmap illustrating the distribution of missing values across rows and columns.
        2. A vertical bar plot displaying the percentage of missing values for each column.

        """
         
        plt.figure(figsize=(20, 10))
        sns.heatmap(self.df.isnull(), cbar=False, cmap="coolwarm") #colour bar removed for clearer heatmap
        plt.title("Heatmap of Null Values in DataFrame")
        plt.xlabel("Columns")
        plt.ylabel("Rows")
        plt.title('Missing Values Percentage per Column')  
        plt.xticks(rotation=90, ha='center', fontsize=10) #rotates to vertical to make titles fit
        plt.tight_layout() #stops column titles from being clipped
        plt.show()
        
        plt.figure(figsize=(16, 9))
        missing_percentage = (self.df.isnull().sum() / len(self.df)) * 100
        missing_percentage = missing_percentage[missing_percentage > 0] #filters out columns with no missing values
        if not missing_percentage.empty:
            missing_percentage.sort_values().plot(kind='bar', color='skyblue') 
            plt.xlabel('Columns')
            plt.ylabel('Percentage of Missing Values')
            plt.title('Missing Values Percentage per Column')
            plt.xticks(rotation=0, ha='right')  #rotates x-axis labels
            plt.show()
        else:
            print("No missing values to plot.") #else statement added for once null values removed to reuse same method

    def plot_distribution(self, column):

        """
        Generates a histogram to visualise the distribution of data in the specified column of the DataFrame to understand skewness of data.

        Parameters:
            column (str): The name of the column for which the distribution is to be plotted.
        
        """

        plt.figure(figsize=(16, 9))
        sns.histplot(self.df[column], kde=True)
        plt.title(f'Distribution of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.show()

    def plot_scatter_plot(self, column):

        """
        Generates a scatter plot to visualise the distribution of data in the specified column of the DataFrame to inspect outliers. 

        Parameters:
            column (str): The name of the column for which the distribution is to be plotted.
        
        """

        plt.figure(figsize=(16, 9))
        sns.scatterplot(x=self.df.index, y=self.df[column], alpha=0.5)
        plt.title(f'Scatter Plot of {column}')
        plt.xlabel('Index')
        plt.ylabel(column)
        plt.show()

    def plot_correlation_matrix(self):

        """
        Generates a heatmap to visualise the correlation of data. 
        
        """

        numeric_data = self.df.select_dtypes(include=['float64', 'int64'])
        correlation_matrix = numeric_data.corr()
        
        plt.figure(figsize=(16, 9))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
        plt.title('Correlation Matrix')
        plt.show()
