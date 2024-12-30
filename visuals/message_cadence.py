from helpers.db import Message, MessagesDB
from analysis.timeseries_analysis import messages_per_period
import matplotlib.pyplot as plt


def plot_message_cadence(db: MessagesDB, messages: list[Message]):
    """Generate and display plot of messages per user per week"""
    messages_by_user = db.separate_messages_by_user(messages)
    df = messages_per_period(messages_by_user, "W")

    plt.figure(figsize=(10, 6))
    for user in df.columns:
        plt.plot(df.index, df[user], label=user)

    plt.xlabel("Week")
    plt.ylabel("Number of Messages")
    plt.title("Messages per Week by User")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    plot_message_cadence()
