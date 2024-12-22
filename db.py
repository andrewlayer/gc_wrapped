import sqlite3
import os
from pathlib import Path
import json
from collections import defaultdict
from datetime import datetime, timedelta


def load_contact_map():
    with open("contact_map.json", "r") as f:
        return json.load(f)


def get_contact_name(sender_id: str, contact_map: dict) -> str:
    for name, identifiers in contact_map.items():
        if sender_id in identifiers:
            return name
    return sender_id

APPLE_EPOCH = datetime(2001, 1, 1)

def apple_time_to_datetime(apple_timestamp: int) -> datetime:
    """Convert Apple's nanosecond timestamp to Python datetime"""
    seconds_since_epoch = (
        apple_timestamp / 1_000_000_000
    )  # Convert nanoseconds to seconds
    return APPLE_EPOCH + timedelta(seconds=seconds_since_epoch)


class MessagesDB:
    def __init__(self):
        self.db_path = "chat.db"  # Updated to use local file
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            return True
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute_query(self, query, params=()):
        """Execute SQL query and return results"""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None

    def get_schema(self):
        """Return complete database schema information"""
        schema_query = """
        SELECT 
            m.type,
            m.name,
            m.tbl_name,
            m.sql
        FROM sqlite_master m
        WHERE m.sql IS NOT NULL
        ORDER BY m.type, m.name;
        """

        try:
            results = self.execute_query(schema_query)
            if results:
                schema_info = {}
                for type_, name, tbl_name, sql in results:
                    if type_ not in schema_info:
                        schema_info[type_] = []
                    schema_info[type_].append(
                        {"name": name, "table": tbl_name, "sql": sql}
                    )
                return schema_info
            return None
        except sqlite3.Error as e:
            print(f"Error fetching schema: {e}")
            return None

    def get_chat_messages(self, chat_identifier: str, start_date=None, end_date=None) -> list:
        """
        Get all messages from a specific group chat with sender names
        Args:
            chat_identifier: The chat identifier (typically the group chat name or ID)
        Returns:
            List of tuples containing message data with sender names
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
            ORDER BY message.date DESC
        """

        try:
            results = self.execute_query(query, (chat_identifier,))
            if not results:
                return []

            contact_map = load_contact_map()
            mapped_results = []

            # Format and Filter DB Results
            for result in results:
                row_id, text, type, date, is_emote, is_from_me, sender_id = result

                # If the messages was sent from the db owner, there will be no associated handle.
                # So we add "Me" to the name map for the db owner.
                if is_from_me and sender_id is None:
                    sender_id = "Me"
                
                # Only include dates within the specified daterange
                date = apple_time_to_datetime(date)
                if date and start_date and date.date() < start_date:
                    continue
                if date and end_date and date.date() > end_date:
                    continue

                sender_name = get_contact_name(sender_id, contact_map)
                mapped_results.append({
                    "row_id": row_id,
                    "text": text,
                    "type": type,
                    "date": date,
                    "is_emote": is_emote,
                    "sender_name": sender_name
                })

            return mapped_results
        except sqlite3.Error as e:
            print(f"Error fetching messages: {e}")
            return []
    
    @staticmethod
    def get_chat_messages_by_user(chat_messages: list) -> dict:
        """
        'Armaan': [('Hello', '2021-01-01'), ('Hi', '2021-01-02')],
        'Bob': [('Hey', '2021-01-03')]
        """
        chat_messages_by_user = defaultdict(list)

        for message in chat_messages:
            sender_name = message["sender_name"]
            chat_messages_by_user[sender_name].append(message)
        
        return chat_messages_by_user


    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
