import os
from datetime import datetime
from dotenv import load_dotenv
from analysis.embedding_analysis import get_embeddings
from helpers.db import MessagesDB
from helpers.pdf_report import ReportContent, create_pdf_report
from helpers.utils import figure_to_tempfile
from visuals.clusters import plot_clusters
from visuals.message_cadence import plot_message_cadence

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

        fig = plot_message_cadence(raw_messages)
        file = figure_to_tempfile(fig)

        report = ReportContent(
            content=file,
            title="Activity",
            description="As you can tell, the number of messages per week by user varies greatly.  Our biggest slacker in the GC is cooper, but Andrew is not far behind.",
        )

        messages_w_embeddings = get_embeddings(raw_messages)

        fig2, description = plot_clusters(messages_w_embeddings)
        file2 = figure_to_tempfile(fig2)

        report2 = ReportContent(
            content=file2,
            title="Biggest Topics",
            description=description,
        )

        create_pdf_report(
            PDF_OUTPUT_PATH,
            [report, report2],
        )


if __name__ == "__main__":
    main()
