import pandas as pd
import datetime
import matplotlib.pyplot as plt


from db import MessagesDB, load_contact_map
from constants import AP_SQUAD_ID

import pandas as pd

def participant_messages_per_period(messages_dict, period='W'):
    """
    Returns dataframe of messages per period (Week, month, year etc) per gc participant
    
    'D': Daily
    'W': Weekly
    'M': Monthly
    'Q': Quarterly
    'Y': Yearly
    """

    # Create an empty DataFrame to store the results
    df = pd.DataFrame()

    # Iterate over each user and their messages
    for user, messages in messages_dict.items():
        if not user:
            continue
        # Extract the dates from the messages
        dates = [msg['date'] for msg in messages]
        # Create a DataFrame for the current user with the dates
        user_df = pd.DataFrame(dates, columns=['date'])
        # Set the date column as the index
        user_df['date'] = pd.to_datetime(user_df['date'])
        user_df.set_index('date', inplace=True)
        # Resample the data by week and count the number of messages per week
        user_df = user_df.resample(period).size()
        # Rename the series to the user's name
        user_df.name = user
        # Join the user's data to the main DataFrame
        df = df.join(user_df, how='outer')

    # Fill NaN values with 0
    df.fillna(0, inplace=True)
    return df

# Generate plot of Messages per user per week
def generate_user_activity_plot(chat_id, period_length='W', start_date=None, end_date=None):
    with MessagesDB() as db:
        gc_messages = db.get_chat_messages(chat_id, start_date, end_date)
        messages_by_user = db.separate_messages_by_user(gc_messages)
        df = participant_messages_per_period(messages_by_user, period_length)
        print(df.sum())

        # Plot the dataframe
        plt.figure(figsize=(10, 6))
        for user in df.columns:
            plt.plot(df.index, df[user], label=user)

        plt.xlabel('Week')
        plt.ylabel('Number of Messages')
        plt.title('Messages per Week by User')
        plt.legend()
        plt.grid(True)
        plt.show()

generate_user_activity_plot(AP_SQUAD_ID, period_length='W', start_date=None, end_date=datetime.date(2021, 12, 31))
