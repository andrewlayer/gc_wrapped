import os
import sqlite3
import json
from datetime import datetime
from typing import List, Optional
from tqdm import tqdm
from helpers.db import Message
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def get_embeddings(
    messages: List[Message], use_cached: bool = True, limit: Optional[int] = None
) -> List[Message]:
    project_cache_path = os.path.join(os.getcwd(), "cached")
    os.makedirs(project_cache_path, exist_ok=True)
    db_path = os.path.join(project_cache_path, "cached.db")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table with full message schema
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cached_messages (
            row_id INTEGER PRIMARY KEY,
            text TEXT,
            type INTEGER,
            date TEXT,
            is_emote BOOLEAN,
            embedding TEXT,
            sender_name TEXT
        )
    """
    )
    conn.commit()

    sample_messages = messages[:limit] if limit is not None else messages
    updated_messages = []

    for msg in tqdm(sample_messages, desc="Processing messages"):
        if use_cached:
            cursor.execute(
                """SELECT * FROM cached_messages WHERE row_id = ?""", (msg.row_id,)
            )
            row = cursor.fetchone()

            if row and row[5]:
                cached_msg = Message(
                    row_id=row[0],
                    text=row[1],
                    type=row[2],
                    date=datetime.fromisoformat(row[3]),
                    is_emote=bool(row[4]),
                    embedding=row[5],
                    sender_name=row[6],
                )
                updated_messages.append(cached_msg)
                continue

        # Get new embedding

        if msg.text:
            response = client.embeddings.create(
                input=msg.text or "", model="text-embedding-3-small"
            )
            emb = response.data[0].embedding
        else:
            emb = None

        # Create new message with embedding
        new_msg = msg.model_copy(update={"embedding": str(emb)})

        # Cache the full message
        cursor.execute(
            """INSERT OR REPLACE INTO cached_messages 
               (row_id, text, type, date, is_emote, embedding, sender_name)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                new_msg.row_id,
                new_msg.text,
                new_msg.type,
                new_msg.date.isoformat(),
                new_msg.is_emote,
                new_msg.embedding,
                new_msg.sender_name,
            ),
        )
        conn.commit()
        updated_messages.append(new_msg)

    if limit is not None:
        updated_messages.extend(messages[limit:])

    conn.close()
    return updated_messages
