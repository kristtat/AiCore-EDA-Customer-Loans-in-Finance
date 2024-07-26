import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class Visualisations:

    """
    A class containing methods to visualise data in the Pandas DataFrame to enable business intelligence.

    Methods:
        __init__(self, credentials): 
            Initialises the DataFrameInfo object with a given DataFrame.

        current_loan_recovery(self):
            Calculates what percentage of loans are recovered against the investor funding and the total amount funded currently.

        future_loan_recovery(self):
            Calculates what percentage of loans would be recovered against the investor funding and the total amount funded 6 months in the future.

        def loan_recovery_graphs(self):
            A bar chart representing what percentage of loans are recovered against the investor funded and the total amount funded currently and in 6 months.

        losses_calc(self):
            Calculates what percentage of loans are a loss to the company and the total amount that was paid towards these loans before being charged off.

        display_charged_off_loans_info(self):
            Displays calculations from losses_calc() method.

        projected_loss_calc(self):
            Calculates the projected loss for charged off loans.

        visualise_projected_loss(self):
            Visualises the projected loss for charged off loans.

        at_risk_customers_calculation(self):
            Calculates the percentage of clients behind on their loans, total number of these clients, how much loss company would incur if their loans were charged off
        and projected loss if clients were to finish full term of loan.

        at_risk_customers_visualisation(self):
            Visualises the at_risk_customers_calculation() calculations.

        create_subset(self):
            Creates subset of users who may not be able to pay off their loans.

        analyse_grade(self):
            Visualises the correlation between loan grade, charged off loans and late loans.

        analyse_purpose(self):
            Visualises the correlation between loan purpose, charged off loans and late loans.
            
        analyse_home_ownership(self):
            Visualises the correlation between home ownership and charged off loans and late loans.
       
    
    """

    def __init__(self, df):
        """
        Initialises the RDSDatabaseConnector with given credentials.

        Parameters:
            credentials(dict): A dictionary containing database connection details.
        
        """
        self.df = df

    
    def current_loan_recovery(self):

        """

        Calculates what percentage of loans are recovered against the investor funding and the total amount funded currently.

        Returns:
            recovered_percentage, recovered_investor_percentage (tuple): Tuple of floats representing the average recovery 
            percentage for the total funded amounts and the investor funded amounts of all loans.

        """


        df_funded = self.df[(self.df['funded_amount'] > 1) & (self.df['funded_amount_inv'] > 1)]
    
        if df_funded.empty:
            print("No data available.")
            return None, None
    
        recovered_percentage = (df_funded['total_payment'] / df_funded['funded_amount'] * 100).mean()
        recovered_investor_percentage = (df_funded['total_payment'] / df_funded['funded_amount_inv'] * 100).mean()
    
        return recovered_percentage, recovered_investor_percentage

    def future_loan_recovery(self):

        """

        Calculates what percentage of loans would be recovered against the investor funding and the total amount funded 6 months in the future.

        Returns:
            future_recovered_percentage, future_recovered_investor_percentage (tuple): Tuple of floats representing the average recovery 
            percentage for the total funded amounts and the investor funded amounts of all loans for a 6 month projection.

        """

        df_funded = self.df[(self.df['funded_amount'] > 1) & (self.df['funded_amount_inv'] > 1)]
        monthly_recovery_rate = df_funded['total_payment'].sum() / (df_funded['funded_amount'].sum() * df_funded['term'].mean())
        future_recovered_percentage = (df_funded['total_payment'] / df_funded['funded_amount'] * 100).mean() + (monthly_recovery_rate * 6)
        future_recovered_investor_percentage = (df_funded['total_payment'] / df_funded['funded_amount_inv'] * 100).mean() + (monthly_recovery_rate * 6)
        return future_recovered_percentage, future_recovered_investor_percentage


    def loan_recovery_graphs(self):

        """

        A bar chart representing what percentage of loans are recovered against the investor funded and the total amount funded currently and in 6 months.

        """
        recovered_percentage, recovered_investor_percentage = self.current_loan_recovery()
        print(f"Current Recovered Percentage: {recovered_percentage:.2f}%")
        print(f"Current Recovered Investor Percentage: {recovered_investor_percentage:.2f}%")

        future_recovered_percentage, future_recovered_investor_percentage = self.future_loan_recovery()
        print(f"Future Recovered Percentage: {future_recovered_percentage:.2f}%")
        print(f"Future Recovered Investor Percentage: {future_recovered_investor_percentage:.2f}%")

        fig, ax = plt.subplots(figsize=(20, 16))
        bars = ax.bar(['Total Funded (Current)', 'Investor Funded (Current)', 'Total Funded (6 months)', 'Investor Funded (6 months)'],
                      [recovered_percentage, recovered_investor_percentage, future_recovered_percentage, future_recovered_investor_percentage], 
                      color=['blue', 'green', 'blue', 'green'])
        ax.set_ylabel('Recovered Percentage')
        ax.set_title('Current and Future Loan Recovery Percentages')

        for bar, percentage in zip(bars, [recovered_percentage, recovered_investor_percentage, future_recovered_percentage, future_recovered_investor_percentage]):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height, f'{percentage:.2f}%', ha='center', va='bottom')

        plt.show()

    def losses_calc(self):

        """

        Calculates what percentage of loans are a loss to the company and the total amount that was paid towards these loans before being charged off.

        Returns:
            charged_off_percentage, total_paid_charged_offe (tuple): Tuple of floats representing the percentage of total loans and the total sum of money paid 
            towards the loans before being charged off.

        """

        charged_off = self.df[self.df['loan_status'] == 'Charged Off']
        total_loans = len(self.df)
        charged_off_loans = len(charged_off)
        charged_off_percentage = (charged_off_loans / total_loans) * 100
        total_paid_charged_off = charged_off['total_payment'].sum()
        
        return charged_off_percentage, total_paid_charged_off

    def display_charged_off_loans_info(self):

        """

        Displays calculations from losses_calc() method.

        """

        charged_off_percentage, total_paid_charged_off = self.losses_calc()
        print(f"Percentage of Charged Off Loans: {charged_off_percentage:.2f}%")
        print(f"Total Amount Paid  By Customers Towards Charged Off Loans: £{total_paid_charged_off:.2f}")
    

    def projected_loss_calc(self):

        """
        Calculates the projected loss for charged off loans.

        Returns:
        projected_loss, charged_off(tuple): Tuple of floats representing the projected loss based on charged-off loans and DataFrame containing the charged-off loans.
        
        """

        charged_off = self.df[self.df['loan_status'] == 'Charged Off']
        projected_revenue = charged_off['instalment'] * charged_off['term']

        total_paid_charged_off = charged_off['total_payment'].sum()
        total_projected_revenue = projected_revenue.sum()
        projected_loss = total_projected_revenue - total_paid_charged_off

        return projected_loss, charged_off
        

    def visualise_projected_loss(self):

        """
        Visualises the projected loss for charged off loans.
        
        """

        projected_loss, charged_off_details = self.projected_loss_calc()

        print(f"Total Projected Loss: ${projected_loss:.2f}")


    def at_risk_customers_calculation(self):

        """
        Calculates the percentage of clients behind on their loans, total number of these clients, how much loss company would incur if their loans were charged off
        and projected loss if clients were to finish full term of loan.

        Returns:
        late_loans_percentage, late_loans_count, projected_loss_if_charged_off, projected_loss_if_full_term(tuple): Tuple of floats and an integer representing the 
        above figures.
        
        
        """

        late_customers = ["Late (16-30 days)", "Late (31-120 days)", "In Grace Period"]
        late_loans = self.df[self.df['loan_status'].isin(late_customers)]

        #percentage of late loans
        total_loans = len(self.df)
        late_loans_num = len(late_loans)
        late_loans_percentage = (late_loans_num / total_loans) * 100

        #projected loss if loan charged off
        projected_revenue = late_loans['instalment'] * late_loans['term']
        total_paid = late_loans['total_payment']
        projected_loss_if_charged_off = (projected_revenue - total_paid).sum()
    
        #projected loss if customers finish the full loan term
        total_projected_revenue = projected_revenue.sum()
        total_paid_amount = total_paid.sum()
        projected_loss_if_full_term = total_projected_revenue - total_paid_amount
      
        return (late_loans_percentage, late_loans_num, projected_loss_if_charged_off, projected_loss_if_full_term)

    def at_risk_customers_visualisation(self):

        """

        Visualises the at_risk_customers_calculation() calculations.
        
        """

        late_loans_percentage, late_loans_num, projected_loss_if_charged_off, projected_loss_if_full_term = self.at_risk_customers_calculation()


        print(f"Percentage of Late Loans: {late_loans_percentage:.2f}%")
        print(f"Total Number of Late Loans: {late_loans_num}")
        print(f"Total Projected Loss if Marked as Charged Off: £{projected_loss_if_charged_off:.2f}")
        print(f"Total Projected Loss if Loans Finish Full Term: £{projected_loss_if_full_term:.2f}") # both produce same outcome, check calculation


    def create_subset(self):

        """
        Creates subset of users who may not be able to pay off their loans.
        
        """
        charged_off_statuses = ['Charged Off']
        at_risk_customers = ['Late (31-120 days)', 'Late (16-30 days)', 'In Grace Period']
        self.df_charged_off = self.df[self.df['loan_status'].isin(charged_off_statuses)]
        self.df_at_risk = self.df[self.df['loan_status'].isin(at_risk_customers)]

    def analyse_grade(self):

        """
        Visualises the correlation between loan grade, charged off loans and late loans.
        
        """
        fig, ax = plt.subplots(1, 2, figsize=(14, 6))

        sns.countplot(data=self.df_charged_off, x='grade', ax=ax[0], order=sorted(self.df['grade'].unique()))
        ax[0].set_title('Loan Grade - Charged Off')
        ax[0].set_xlabel('Grade')
        ax[0].set_ylabel('Count')

        sns.countplot(data=self.df_at_risk, x='grade', ax=ax[1], order=sorted(self.df['grade'].unique()))
        ax[1].set_title('Loan Grade - At Risk')
        ax[1].set_xlabel('Grade')
        ax[1].set_ylabel('Count')

        plt.tight_layout()
        plt.show()

    def analyse_purpose(self):

        """
        Visualises the correlation between loan purpose, charged off loans and late loans.
        
        """

        fig, ax = plt.subplots(1, 2, figsize=(14, 6))

        sns.countplot(data=self.df_charged_off, y='purpose', ax=ax[0], order=self.df['purpose'].value_counts().index)
        ax[0].set_title('Loan Purpose - Charged Off')
        ax[0].set_xlabel('Count')
        ax[0].set_ylabel('Purpose')

        sns.countplot(data=self.df_at_risk, y='purpose', ax=ax[1], order=self.df['purpose'].value_counts().index)
        ax[1].set_title('Loan Purpose - At Risk')
        ax[1].set_xlabel('Count')
        ax[1].set_ylabel('Purpose')

        plt.tight_layout()
        plt.show()

    def analyse_home_ownership(self):

        """
        Visualises the correlation between home ownership and charged off loans and late loans.
        
        """

        fig, ax = plt.subplots(1, 2, figsize=(14, 6))

        sns.countplot(data=self.df_charged_off, x='home_ownership', ax=ax[0], order=self.df['home_ownership'].value_counts().index)
        ax[0].set_title('Home Ownership- Charged Off')
        ax[0].set_xlabel('Home Ownership')
        ax[0].set_ylabel('Count')

        sns.countplot(data=self.df_at_risk, x='home_ownership', ax=ax[1], order=self.df['home_ownership'].value_counts().index)
        ax[1].set_title('Home Ownership - At Risk')
        ax[1].set_xlabel('Home Ownership')
        ax[1].set_ylabel('Count')

        plt.tight_layout()
        plt.show()

