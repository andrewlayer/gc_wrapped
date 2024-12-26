import os
from datetime import datetime
from dotenv import load_dotenv
from helpers.db import MessagesDB
from analysis.timeseries_analysis import messages_per_period, plot_timeseries

load_dotenv()

AP_SQUAD_ID = os.getenv("AP_SQUAD_ID")
CHAT_DB_PATH = os.getenv("CHAT_DB_PATH")
CONTACT_MAP_PATH = os.getenv("CONTACT_MAP_PATH")
START_DATE = datetime.strptime(os.getenv("START_DATE"), "%Y-%m-%d")
END_DATE = datetime.strptime(os.getenv("END_DATE"), "%Y-%m-%d")


def main():
    with MessagesDB(db_path=CHAT_DB_PATH, contact_map_path=CONTACT_MAP_PATH) as db:
        raw_messages = db.get_chat_messages(AP_SQUAD_ID, START_DATE, END_DATE)
        messages_by_user = db.separate_messages_by_user(raw_messages)
        timeseries_df = messages_per_period(messages_by_user, period="W")
        fig = plot_timeseries(timeseries_df)
        fig.show()


if __name__ == "__main__":
    main()
