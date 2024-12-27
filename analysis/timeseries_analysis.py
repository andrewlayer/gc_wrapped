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


def plot_timeseries(df, title="Messages Over Time"):
    """Plots a time-series line chart for each user in the DataFrame."""
    fig, ax = plt.subplots(figsize=(10, 5))

    # Validate data exists
    if df.empty or len(df.columns) == 0:
        print("No data to plot")
        return fig

    # Only plot columns with data
    has_data = False
    for col in df.columns:
        if df[col].sum() > 0:  # Only plot if user has messages
            ax.plot(df.index, df[col], label=col)
            has_data = True

    ax.set_xlabel("Date")
    ax.set_ylabel("# Messages")
    ax.set_title(title)
    ax.grid(True)

    if has_data:  # Only add legend if we plotted data
        ax.legend(loc="upper left", bbox_to_anchor=(1, 1))

    plt.tight_layout()
    return fig
