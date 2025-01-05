import os
import sqlite3
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from helpers.utils import apple_time_to_datetime, get_contact_name, load_contact_map


class Message(BaseModel):
    """Single message from iMessage database"""

    row_id: int
    text: Optional[str] = None
    type: int
    date: datetime
    is_emote: bool = False
    embedding: Optional[str] = None
    sender_name: str

    class Config:
        frozen = False

    def to_dict(self):
        """Serialize to dictionary"""
        return self.model_dump()


class MessagesDB:
    """Manages connection to local chat.db and provides methods to query chat messages"""

    def __init__(
        self,
        db_path="chat.db",
        contact_map_path="contact_map.json",
        cached_db_path="./cached.db",
    ):
        self.db_path = db_path
        self.contact_map = load_contact_map(contact_map_path)
        self.conn = None
        self.cursor = None
        self.cached_db_path = cached_db_path

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
        """Safely executes SQL queries and returns results"""
        if not self.cursor:
            print("Cursor is not available.")
            return None
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None

    def __create_cache(self, messages: List[Message]):
        """Create and populate cache database with messages"""

        # Connect to cache database
        cache_conn = sqlite3.connect("./cached.db")
        cache_cursor = cache_conn.cursor()

        # Create messages table if it doesn't exist
        cache_cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                row_id INTEGER PRIMARY KEY,
                text TEXT,
                type INTEGER,
                date TIMESTAMP,
                is_emote BOOLEAN,
                embedding TEXT,
                sender_name TEXT
            )
        """
        )

        try:
            # Insert messages that don't exist in cache
            for message in messages:
                cache_cursor.execute(
                    """
                    INSERT OR IGNORE INTO messages 
                    (row_id, text, type, date, is_emote, embedding, sender_name)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        message.row_id,
                        message.text,
                        message.type,
                        message.date.isoformat(),
                        message.is_emote,
                        message.embedding,
                        message.sender_name,
                    ),
                )

            cache_conn.commit()

        finally:
            cache_cursor.close()
            cache_conn.close()

    def get_chat_messages(
        self,
        chat_identifier: Optional[str] = None,
        start_date=None,
        end_date=None,
        n: Optional[int] = None,
        use_cached: bool = True,
    ) -> List[Message]:
        """Get messages with optional chat and date filtering"""
        all_messages = []
        latest_cached_date = None

        # Load cached messages if enabled
        if use_cached and os.path.exists(self.cached_db_path):
            try:
                cache_conn = sqlite3.connect(self.cached_db_path)
                cache_cursor = cache_conn.cursor()

                date_filter = ""
                params = []
                if start_date:
                    date_filter = "WHERE date >= ?"
                    params.append(start_date.isoformat())
                if end_date:
                    date_filter += (
                        " AND date <= ?" if date_filter else "WHERE date <= ?"
                    )
                    params.append(end_date.isoformat())

                cache_cursor.execute(
                    f"""
                    SELECT row_id, text, type, date, is_emote, embedding, sender_name 
                    FROM messages
                    {date_filter}
                    ORDER BY date DESC
                """,
                    params,
                )

                for row in cache_cursor.fetchall():
                    msg = Message(
                        row_id=row[0],
                        text=row[1],
                        type=row[2],
                        date=datetime.fromisoformat(row[3]),
                        is_emote=row[4],
                        embedding=row[5],
                        sender_name=row[6],
                    )
                    all_messages.append(msg)

                if all_messages:
                    latest_cached_date = max(msg.date for msg in all_messages)

            finally:
                cache_cursor.close()
                cache_conn.close()

        # Build query for original database
        date_conditions = []
        params = []

        if chat_identifier:
            date_conditions.append("chat.chat_identifier = ?")
            params.append(chat_identifier)

        if latest_cached_date:
            # Only get messages newer than cache
            cache_ns = int(
                (latest_cached_date - datetime(2001, 1, 1)).total_seconds()
                * 1_000_000_000
            )
            date_conditions.append("message.date > ?")
            params.append(cache_ns)
        elif start_date:
            start_ns = int(
                (start_date - datetime(2001, 1, 1)).total_seconds() * 1_000_000_000
            )
            date_conditions.append("message.date >= ?")
            params.append(start_ns)

        if end_date:
            end_ns = int(
                (end_date - datetime(2001, 1, 1)).total_seconds() * 1_000_000_000
            )
            date_conditions.append("message.date <= ?")
            params.append(end_ns)

        where_clause = " AND ".join(date_conditions) if date_conditions else "1=1"

        query = f"""
            SELECT
                message.ROWID,
                message.text,
                message.type,
                message.date,
                message.is_emote,
                message.is_from_me,
                handle.id as sender_id,
                message.attributedBody
            FROM message
            {"JOIN chat_message_join ON chat_message_join.message_id = message.ROWID" if chat_identifier else ""}
            {"JOIN chat ON chat.ROWID = chat_message_join.chat_id" if chat_identifier else ""}
            LEFT JOIN handle ON message.handle_id = handle.ROWID
            WHERE {where_clause}
            ORDER BY message.date DESC
        """

        results = self.execute_query(query, tuple(params))
        if results:
            new_messages = []
            for res in results:
                (
                    row_id,
                    text,
                    msg_type,
                    date_val,
                    is_emote,
                    is_from_me,
                    sender_id,
                    attributed_body,
                ) = res

                if text is None and attributed_body:
                    try:
                        attributed_body = attributed_body.decode(
                            "utf-8", errors="replace"
                        )
                        if "NSNumber" in attributed_body:
                            attributed_body = attributed_body.split("NSNumber")[0]
                            if "NSString" in attributed_body:
                                attributed_body = attributed_body.split("NSString")[1]
                                if "NSDictionary" in attributed_body:
                                    attributed_body = attributed_body.split(
                                        "NSDictionary"
                                    )[0]
                                    text = attributed_body[6:-12]
                    except:
                        continue

                if is_from_me and sender_id is None:
                    sender_id = "Me"

                if not text:
                    continue

                date_obj = apple_time_to_datetime(date_val)
                sender_name = get_contact_name(sender_id, self.contact_map)

                if sender_name is None:
                    continue

                msg = Message(
                    row_id=row_id,
                    text=text,
                    type=msg_type,
                    date=date_obj,
                    is_emote=bool(is_emote),
                    sender_name=sender_name,
                )
                new_messages.append(msg)
                all_messages.append(msg)

            # Cache new messages if found
            if use_cached and new_messages:
                self.__create_cache(new_messages)

        # Apply limit if specified
        if n is not None:
            all_messages = all_messages[:n]

        return sorted(all_messages, key=lambda x: x.date, reverse=True)
