import os
from typing import Tuple

from pydantic import BaseModel
from helpers.db import Message
from helpers.clients import openai_client
from analysis.embedding_analysis import cluster_messages
import matplotlib.pyplot as plt
import numpy as np


class ClusterMetadata(BaseModel):
    cluster_name: str
    cluster_quotes: list[str]


def _name_clusters(
    message_map: dict[int, Message], cluster_map: dict[int, int]
) -> ClusterMetadata:
    message_clusters = {}

    for row_id, message in message_map.items():
        cluster = cluster_map[row_id]
        if cluster not in message_clusters:
            message_clusters[cluster] = []
        message_clusters[cluster].append(message.sender_name + ": " + message.text)

    cluster_metadata = {}
    for cluster, messages in message_clusters.items():
        sample_messages = np.random.choice(
            messages, size=min(100, len(messages)), replace=False
        )

        # Prepare prompt
        prompt = """Based on the following messages, generate a name for this cluster and 
        put it in cluster_name.  Then choose your favorite 1-2 text qoutes and place them 
        in cluster_quotes (be sure to preprend with the name of the sender):\n\n"""
        prompt += "\n".join(sample_messages)

        # Call OpenAI API
        completion = openai_client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates short, concise names.",
                },
                {"role": "user", "content": prompt},
            ],
            response_format=ClusterMetadata,
        )

        cluster_metadata[cluster] = completion.choices[0].message.parsed

    return cluster_metadata


def plot_clusters(
    messages: list[Message], num_clusters: int = 5
) -> Tuple[plt.Figure, str]:
    """Generate and display plot of clustered messages"""
    tsne_results, labels, tsne_df = cluster_messages(messages, num_clusters)

    cluster_metadata = _name_clusters(tsne_df["message"], tsne_df["cluster"])

    fig = plt.figure(figsize=(10, 6))
    scatter = plt.scatter(
        tsne_results[:, 0], tsne_results[:, 1], c=labels, cmap="viridis", alpha=0.6
    )
    plt.xlabel("TSNE Component 1")
    plt.ylabel("TSNE Component 2")
    plt.title(f"Message Clusters (k={num_clusters})")

    # Create a legend with cluster names
    handles, _ = scatter.legend_elements()
    legend_labels = [
        cluster_metadata[label].cluster_name for label in range(num_clusters)
    ]
    plt.legend(handles, legend_labels, title="Clusters")

    plt.grid(True)
    plt.tight_layout()

    # Build the description with proper ReportLab markup
    description = "<b>Some of the best quotes from each topic:</b>" "<br/>"

    for _, metadata in cluster_metadata.items():
        # Add cluster name with proper spacing
        description += "<br/>" f"<b>{metadata.cluster_name}</b>" "<br/>"

        # Add quotes with bullet points
        for quote in metadata.cluster_quotes:
            sanitized_quote = (
                quote.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            )
            description += f"&bull; {sanitized_quote}<br/>"

    return fig, description
