import os
from datetime import datetime
from dotenv import load_dotenv
from analysis.embedding_analysis import get_embeddings
from helpers.db import MessagesDB
from analysis.timeseries_analysis import messages_per_period, plot_timeseries
from helpers.pdf_report import ReportContent, create_pdf_report
from helpers.utils import figure_to_tempfile
from visuals.clusters import plot_clusters

load_dotenv()

CHAT_ID = os.getenv("CHAT_ID")
CHAT_DB_PATH = os.getenv("CHAT_DB_PATH")
CONTACT_MAP_PATH = os.getenv("CONTACT_MAP_PATH")
PDF_OUTPUT_PATH = os.getenv("PDF_OUTPUT_PATH")
START_DATE = datetime.strptime(os.getenv("START_DATE"), "%Y-%m-%d")
END_DATE = datetime.strptime(os.getenv("END_DATE"), "%Y-%m-%d")


def main():
    with MessagesDB(db_path=CHAT_DB_PATH, contact_map_path=CONTACT_MAP_PATH) as db:
        raw_messages = db.get_chat_messages(CHAT_ID, START_DATE, END_DATE)
        messages_by_user = db.separate_messages_by_user(raw_messages)
        timeseries_df = messages_per_period(messages_by_user, period="W")

        if timeseries_df.empty:
            return

        fig = plot_timeseries(timeseries_df)
        file = figure_to_tempfile(fig)

        report = ReportContent(
            content=file,
            title="Messages per Week by User",
            description="This plot shows the number of messages sent by each user per week.",
        )

        messages_w_embeddings = get_embeddings(raw_messages)

        fig2, description = plot_clusters(messages_w_embeddings)
        file2 = figure_to_tempfile(fig2)

        report2 = ReportContent(
            content=file2,
            title="Message Clusters",
            description=description,
        )

        create_pdf_report(
            PDF_OUTPUT_PATH,
            [report, report2],
        )


if __name__ == "__main__":
    main()
