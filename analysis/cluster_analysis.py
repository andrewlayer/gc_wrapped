import os
import sqlite3
from typing import List, Optional
from tqdm import tqdm
from helpers.db import Message
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def get_embeddings(
    messages: List[Message], use_cached: bool = True, limit: Optional[int] = None
) -> List[Message]:
    """
    Checks for cached embeddings in `cached/cached.db` if use_cached=True.
    If an embedding for a message row_id isn't found (or use_cached=False),
    calls OpenAI to create one. Caches new embeddings in the same database.

    Args:
        messages: List of Message objects to embed
        use_cached: Whether to skip embedding if a cached value exists
        limit: Optional maximum number of messages to embed

    Returns:
        List of updated Message objects (with .embedding fields filled in)
    """
    # Ensure we have a local directory to store the cache
    project_cache_path = os.path.join(os.getcwd(), "cached")
    os.makedirs(project_cache_path, exist_ok=True)
    db_path = os.path.join(project_cache_path, "cached.db")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS message_embeddings (
            row_id INTEGER PRIMARY KEY,
            embedding TEXT
        )
        """
    )
    conn.commit()

    # Decide how many messages to embed
    sample_messages = messages[:limit] if limit is not None else messages

    updated_messages = []
    # Process only the subset (limited) for embeddings
    for msg in tqdm(sample_messages, desc="Embedding messages"):
        row = None
        if use_cached:
            cursor.execute(
                "SELECT embedding FROM message_embeddings WHERE row_id = ?",
                (msg.row_id,),
            )
            row = cursor.fetchone()

        if row:
            # Cached embedding found
            msg.embedding = row[0]
        else:
            # Call OpenAI to get embedding
            response = client.embeddings.create(
                input="Your text string goes here", model="text-embedding-3-small"
            )
            emb = response.data[0].embedding

            # Store embedding in DB
            cursor.execute(
                "INSERT OR REPLACE INTO message_embeddings (row_id, embedding) VALUES (?, ?)",
                (msg.row_id, str(emb)),
            )
            conn.commit()

            msg.embedding = str(emb)

        updated_messages.append(msg)

    # Append any remaining messages unmodified (if limit was set)
    if limit is not None and limit < len(messages):
        updated_messages.extend(messages[limit:])

    conn.close()
    return updated_messages
