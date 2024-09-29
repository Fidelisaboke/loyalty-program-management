""" Main Program """

from functions import *

EXCEL_DIR = 'excel/'

if __name__ == "__main__":
    df = pd.read_csv("purchasing-behaviors.csv")

    # Get loyal customers and generate personalized emails
    filtered_df = get_loyal_customers(df)
    generate_personalized_emails(filtered_df)

    # Segment customers
    segment_customers(df)

    # Write to excel
    df.to_excel(f"{EXCEL_DIR}purchasing-behaviors.xlsx")


