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

    def get_chat_messages(
        self,
        chat_identifier: Optional[str] = None,
        start_date=None,
        end_date=None,
        n: Optional[int] = None,
    ) -> List[Message]:
        """Get messages with optional chat and date filtering, limited to n messages if specified"""
        date_conditions = []
        params = []

        if chat_identifier:
            date_conditions.append("chat.chat_identifier = ?")
            params.append(chat_identifier)

        if start_date:
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
            {f"LIMIT {n}" if n is not None else ""}
        """

        results = self.execute_query(query, tuple(params))
        if not results:
            return []

        mapped_results = []
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
                    attributed_body = attributed_body.decode("utf-8", errors="replace")
                    if "NSNumber" in attributed_body:
                        attributed_body = attributed_body.split("NSNumber")[0]
                        if "NSString" in attributed_body:
                            attributed_body = attributed_body.split("NSString")[1]
                            if "NSDictionary" in attributed_body:
                                attributed_body = attributed_body.split("NSDictionary")[
                                    0
                                ]
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

            mapped_results.append(
                Message(
                    row_id=row_id,
                    text=text,
                    type=msg_type,
                    date=date_obj,
                    is_emote=bool(is_emote),
                    sender_name=sender_name,
                )
            )

        return sorted(mapped_results, key=lambda x: x.date)
