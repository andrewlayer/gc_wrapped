from collections import defaultdict
from typing import List
from helpers import db
from helpers.db import Message
from analysis.timeseries_analysis import messages_per_period
import matplotlib.pyplot as plt


def separate_messages_by_sender(
    chat_messages: list[Message],
) -> dict[str, list[Message]]:
    """
    Splits a list of message dicts into dict-of-dicts by user
    """
    messages_by_user = defaultdict(list)
    for msg in chat_messages:
        user = msg.sender_name
        messages_by_user[user].append(msg)
    return messages_by_user


def plot_message_cadence(messages: list[Message], title="Messages Over Time"):

    messages = separate_messages_by_sender(messages)
    df = messages_per_period(messages, period="W")

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
