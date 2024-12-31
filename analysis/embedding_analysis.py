from ast import literal_eval
import os
import sqlite3
from datetime import datetime
from typing import List, Optional, Tuple
import numpy as np
import pandas as pd
from tqdm import tqdm
from helpers.db import Message
from openai import OpenAI
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from helpers.clients import openai_client


class DeserizalizedEmbeddingMessage(Message):
    """Single message from iMessage database"""

    embedding: list[float] = None

    class Config:
        frozen = False


def get_embeddings(
    messages: List[Message],
    use_cached: bool = True,
    limit: Optional[int] = None,
) -> List[DeserizalizedEmbeddingMessage]:
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
    updated_messages: list[Message] = []

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
                    embedding=row[5] if row[5] != "None" else None,
                    sender_name=row[6],
                )
                updated_messages.append(cached_msg)
                continue

        # Get new embedding

        if msg.text:
            response = openai_client.embeddings.create(
                input=msg.text, model="text-embedding-3-small"
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

    for msg in updated_messages:
        if msg.embedding is not None:
            msg.embedding = literal_eval(msg.embedding)

    return updated_messages


def cluster_messages(
    messages: List[DeserizalizedEmbeddingMessage], num_clusters: int = 5
) -> Tuple[np.ndarray, np.ndarray, dict]:

    embeddings = [msg.embedding for msg in messages if msg.embedding is not None]
    messages_with_embeddings = [msg for msg in messages if msg.embedding is not None]

    embeddings_df = pd.DataFrame(embeddings)
    matrix = np.vstack(embeddings_df.values)
    print(matrix.shape)

    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(matrix)
    tsne = TSNE(n_components=2, random_state=0)
    tsne_results = tsne.fit_transform(matrix)

    tsne_df = pd.DataFrame(tsne_results, columns=["x", "y"])
    tsne_df["message"] = messages_with_embeddings
    tsne_df["cluster"] = kmeans.labels_

    return tsne_results, kmeans.labels_, tsne_df.to_dict()
