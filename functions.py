""" This module contains functions used to process the CSV """

import pandas as pd
import string
import random

def get_loyal_customers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get loyal customers from the purchasing behaviours dataframe.
    :param df: The purchasing behaviours dataframe.
    :return: A filtered dataframe containing the new customers
    """
    age_condition = (df['age'] >= 27) & (df['age'] <= 35)
    loyalty_condition = (df['loyalty_score'] > 6.5)
    return df[(age_condition & loyalty_condition)]


def generate_personalized_emails(df: pd.DataFrame) -> None:
    """
    Generate personalized emails
    :param df: The loyal customers dataframe.
    :return: None
    """

    template ="""Dear loyal customer,

You have achieved a high loyalty score of {{loyalty_score}}!
We're excited to offer you a discount of {{discount_percentage}}% on your next purchase!

Your unique discount code is: {{discount_code}}

Enjoy your shopping!

For any issues, please reach out to {{company_email}}

Best regards,
{{company_name}} Team
"""

    personalized_email = template.replace("{{company_name}}", "Best Company")
    personalized_email = personalized_email.replace("{{company_email}}", "bestcompany@example.com")
    personalized_email = personalized_email.replace("{{discount_percentage}}", "50")

    for index, row in df.iterrows():
        loyalty_score = row['loyalty_score']
        discount_code = ''.join(random.choices(string.ascii_letters, k=10))

        personalized_email = personalized_email.replace("{{loyalty_score}}", str(loyalty_score))
        personalized_email = personalized_email.replace("{{discount_code}}", discount_code)

        filename = f"personalized_emails/email_{index}.txt"
        with open(filename, "w") as text_file:
            text_file.write(personalized_email)


def segment_customers(df: pd.DataFrame) -> None:
    """
    Segment customers according to their income, loyalty and purchase frequency
    Customer segmentation:\n
    **HIGH:**\n
    - annual_income > 60000\n
    - loyalty_score > 6.5\n
    - purchase_frequency > 23.5\n
    **MEDIUM:**\n
    - annual_income > 45000 (up to 60000)\n
    - loyalty_score > 4.5 (up to 6.5)\n
    - purchase_frequency > 14.5 (up to 23.5)\n
    **LOW:**\n
    - Below the lower bounds of 'MEDIUM'
    :param df: The purchasing behaviours dataframe.
    """

    # High condition mask
    high_income_mask = df['annual_income'] > 60000
    high_loyalty_mask = df['loyalty_score'] > 6.5
    high_purchase_frequency_mask = df['purchase_frequency'] > 23.5
    high_condition_mask = high_income_mask & high_loyalty_mask & high_purchase_frequency_mask

    # Medium condition mask
    med_income_mask = (45000 < df['annual_income']) & (df['annual_income']<= 60000)
    med_loyalty_mask = (4.5 < df['loyalty_score']) & (df['loyalty_score'] <= 6.5)
    med_purchase_frequency = (14.5 < df['purchase_frequency']) & (df['purchase_frequency'] <= 23.5)
    med_condition_mask = med_income_mask & med_loyalty_mask & med_purchase_frequency

    # Customer tier
    df['customer_tier'] = "Low"

    # Update customer tier
    df.loc[high_condition_mask, 'customer_tier'] = "High"
    df.loc[med_condition_mask, 'customer_tier'] = "Medium"