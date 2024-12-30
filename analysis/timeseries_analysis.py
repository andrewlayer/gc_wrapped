from typing import Dict, List
import pandas as pd
import matplotlib.pyplot as plt

from helpers.db import Message


def messages_per_period(messages_dict: Dict[str, List[Message]], period="W"):
    """
    Resamples message counts over a specified period:
    'D' for daily, 'W' for weekly, 'M' for monthly, etc.
    Returns a pandas DataFrame with each user as a column
    and time as the index.
    """
    df = pd.DataFrame()
    for user, messages in messages_dict.items():
        if not user:
            continue
        user_dates = [msg.date for msg in messages]
        user_df = pd.DataFrame(user_dates, columns=["date"])
        user_df.set_index("date", inplace=True)
        # Resample and count
        user_df = user_df.resample(period).size()
        user_df.name = user
        df = df.join(user_df, how="outer")
    df.fillna(0, inplace=True)
    return df
