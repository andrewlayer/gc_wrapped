import os
from datetime import datetime
from dotenv import load_dotenv
from analysis.embedding_analysis import get_embeddings
from helpers.coverage_check import check_message_coverage
from helpers.db import MessagesDB
from helpers.pdf_report import ReportContent, create_pdf_report
from helpers.utils import figure_to_tempfile
from visuals.clusters import plot_clusters
from visuals.message_cadence import plot_message_cadence
from visuals.sentiments import plot_profanity_stats
from visuals.reactions import plot_reaction_stats

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
            title="Weekly activity",
            description="Weekly activity",
        )

        # messages_w_embeddings = get_embeddings(raw_messages)

        # fig2, description = plot_clusters(
        #     messages_w_embeddings, num_clusters=7, ai_summary=True
        # )
        # file2 = figure_to_tempfile(fig2)

        # report2 = ReportContent(
        #     content=file2,
        #     title="Cluster analysis",
        #     description=description,
        # )

        fig3 = plot_profanity_stats(
            raw_messages, excluded_words={"death", "hell", "damn"}
        )
        file3 = figure_to_tempfile(fig3)

        report3 = ReportContent(
            content=file3,
            title="Profanity usage",
            description="Whoever is the most profane",
        )

        fig4 = plot_reaction_stats(
            raw_messages
        )
        file4 = figure_to_tempfile(fig4)


        report4 = ReportContent(
            content=file4,
            title="Reaction usage",
            description="Whoever uses the most reacts",
        )


        create_pdf_report(
            PDF_OUTPUT_PATH,
            [report, report3, report4]
        )

if __name__ == "__main__":
    main()
