from helpers.db import MessagesDB
from analysis.timeseries_analysis import messages_per_period
import matplotlib.pyplot as plt
from config import AP_SQUAD_ID, CHAT_DB_PATH, CONTACT_MAP_PATH, START_DATE, END_DATE


def plot_message_cadence(db: MessagesDB):
    """Generate and display plot of messages per user per week"""
    gc_messages = db.get_chat_messages(AP_SQUAD_ID, START_DATE, END_DATE)
    messages_by_user = db.separate_messages_by_user(gc_messages)
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
