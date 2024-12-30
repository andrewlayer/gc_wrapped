import os
from typing import TypedDict

from openai import OpenAI
from helpers.db import Message
from analysis.embedding_analysis import cluster_messages
import matplotlib.pyplot as plt
import numpy as np

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def _name_clusters(message_map: dict[int, Message], cluster_map: dict[int, int]) -> str:
    message_clusters = {}

    for row_id, message in message_map.items():
        cluster = cluster_map[row_id]
        if cluster not in message_clusters:
            message_clusters[cluster] = []
        message_clusters[cluster].append(message.text)

    cluster_names = {}
    for cluster, messages in message_clusters.items():
        sample_messages = np.random.choice(
            messages, size=min(100, len(messages)), replace=False
        )

        # Prepare prompt
        prompt = (
            "Based on the following messages, generate a name for this cluster:\n\n"
        )
        prompt += "\n".join(sample_messages)

        # Call OpenAI API
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates short, concise names.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        cluster_names[cluster] = completion.choices[0].message.content

    return cluster_names


def plot_clusters(messages: list[Message], num_clusters: int = 5):
    """Generate and display plot of clustered messages"""
    tsne_results, labels, tsne_df = cluster_messages(messages, num_clusters)

    cluster_names = _name_clusters(tsne_df["message"], tsne_df["cluster"])

    fig = plt.figure(figsize=(10, 6))
    scatter = plt.scatter(
        tsne_results[:, 0], tsne_results[:, 1], c=labels, cmap="viridis", alpha=0.6
    )
    plt.xlabel("TSNE Component 1")
    plt.ylabel("TSNE Component 2")
    plt.title(f"Message Clusters (k={num_clusters})")

    # Create a legend with cluster names
    handles, _ = scatter.legend_elements()
    legend_labels = [cluster_names[label] for label in range(num_clusters)]
    plt.legend(handles, legend_labels, title="Clusters")

    plt.grid(True)
    plt.tight_layout()

    return fig
