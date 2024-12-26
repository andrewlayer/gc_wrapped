import sqlite3
from datetime import datetime, timedelta
import json
from collections import defaultdict
import os
from pathlib import Path


# Helper function
def apple_time_to_datetime(apple_timestamp: int) -> datetime:
    """
    Convert Apple's nanosecond timestamp to Python datetime
    """
    APPLE_EPOCH = datetime(2001, 1, 1)
    seconds_since_epoch = apple_timestamp / 1_000_000_000  # ns to seconds
    return APPLE_EPOCH + timedelta(seconds=seconds_since_epoch)


def load_contact_map(file_path: str) -> dict:
    """
    Load JSON file mapping phone numbers/emails to names
    """
    with open(file_path, "r") as f:
        return json.load(f)


def get_contact_name(sender_id: str, contact_map: dict) -> str:
    """
    Look up the plain-text name for a given phone number/email
    """
    for name, identifiers in contact_map.items():
        if sender_id in identifiers:
            return name
    return sender_id


class MessagesDB:
    """
    Manages connection to local chat.db and provides methods
    to query chat messages
    """

    def __init__(self, db_path="chat.db", contact_map_path="contact_map.json"):
        self.db_path = db_path
        self.contact_map = load_contact_map(contact_map_path)
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute_query(self, query, params=()):
        """
        Safely executes SQL queries and returns results
        """
        if not self.cursor:
            print("Cursor is not available.")
            return None
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None

    def get_chat_messages(
        self, chat_identifier: str, start_date=None, end_date=None
    ) -> list:
        """
        Return messages and associated metadata for a particular chat_identifier,
        optionally constrained by a date range.
        """
        query = """
            SELECT
                message.ROWID,
                message.text,
                message.type,
                message.date,
                message.is_emote,
                message.is_from_me,
                handle.id as sender_id
            FROM message
            JOIN chat_message_join ON chat_message_join.message_id = message.ROWID
            JOIN chat ON chat.ROWID = chat_message_join.chat_id
            LEFT JOIN handle ON message.handle_id = handle.ROWID
            WHERE chat.chat_identifier = ?
            ORDER BY message.date ASC
        """

        results = self.execute_query(query, (chat_identifier,))
        if not results:
            return []

        mapped_results = []
        for (
            row_id,
            text,
            msg_type,
            date_val,
            is_emote,
            is_from_me,
            sender_id,
        ) in results:
            # "Me" for from_me case if handle is null
            if is_from_me and sender_id is None:
                sender_id = "Me"
            date_obj = apple_time_to_datetime(date_val)
            # Filter by date if range is given
            if start_date and date_obj < start_date:
                continue
            if end_date and date_obj > end_date:
                continue

            sender_name = get_contact_name(sender_id, self.contact_map)
            mapped_results.append(
                {
                    "row_id": row_id,
                    "text": text,
                    "type": msg_type,
                    "date": date_obj,
                    "is_emote": is_emote,
                    "sender_name": sender_name,
                }
            )
        return mapped_results

    @staticmethod
    def separate_messages_by_user(chat_messages: list) -> dict:
        """
        Splits a list of message dicts into dict-of-dicts by user
        """
        messages_by_user = defaultdict(list)
        for msg in chat_messages:
            user = msg["sender_name"]
            messages_by_user[user].append(msg)
        return messages_by_user
