import os
import openai
import numpy as np
from sklearn.cluster import KMeans

def embed_messages(messages, api_key):
    """
    Uses OpenAI to embed a list of messages.
    Returns a list of embedding vectors (each a Python list or np.array).
    Note: In practice, you should handle batching & error-checking.
    """
    openai.api_key = api_key
    embeddings = []
    for msg in messages:
        text = msg.get("text", "") or ""
        if not text.strip():
            # For empty text, append a zero vector
            embeddings.append(np.zeros(1536))
            continue
        try:
            response = openai.Embedding.create(
                model="text-embedding-ada-002",
                input=text
            )
            vector = response['data'][0]['embedding']
            embeddings.append(np.array(vector))
        except Exception as e:
            print(f"OpenAI error: {e}")
            embeddings.append(np.zeros(1536))
    return np.array(embeddings)

def cluster_conversations(messages, api_key, n_clusters=5):
    """
    Given a list of messages, embed them, then run KMeans clustering.
    Returns a list of cluster labels (one per message).
    """
    data = embed_messages(messages, api_key)
    if len(data) == 0:
        return []
    # Fit KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(data)
    return labels

def assign_cluster_labels(messages, labels):
    """
    Attach the cluster label to each message for analysis.
    """
    for msg, cluster in zip(messages, labels):
        msg["cluster_label"] = cluster
    return messages 