from typing import List
import matplotlib.pyplot as plt
from helpers.db import Message
from analysis.sentiment_analysis import profanity_freq


def plot_profanity_stats(messages: List[Message], title="Profanity Usage Stats"):
    profanity_data = profanity_freq(messages)
    if not profanity_data:
        fig, ax = plt.subplots(1, 1, figsize=(10, 5))
        ax.text(0.5, 0.5, "No profanity data available", ha="center", va="center")
        return fig

    # Increased figure width for legend
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

    # First subplot
    senders = list(profanity_data.keys())
    frequencies = [data["frequency"] for data in profanity_data.values()]

    # Add labels to bars in first subplot
    bars1 = ax1.bar(senders, frequencies, label=senders)
    ax1.bar_label(bars1, padding=3)
    ax1.set_title("Total Profanity Usage by Sender")
    ax1.set_ylabel("Number of Profane Words")
    ax1.tick_params(axis="x", rotation=45)

    # Second subplot with padding for missing values
    max_words = 3
    bar_width = 0.8
    group_spacing = 2

    for i, sender in enumerate(senders):
        cuss_freq = profanity_data[sender]["cuss_frequency"]
        words = list(cuss_freq.keys())[:max_words]
        counts = list(cuss_freq.values())[:max_words]

        # Pad lists if fewer than max_words
        while len(words) < max_words:
            words.append("")
            counts.append(0)

        x_positions = [x + (i * (max_words + group_spacing)) for x in range(max_words)]
        bars = ax2.bar(x_positions, counts, width=bar_width, label=sender)

        # Add word labels only for non-empty words
        for rect, word in zip(bars, words):
            if word:
                height = rect.get_height()
                ax2.text(
                    rect.get_x() + bar_width / 2,
                    height + 0.5,
                    word,
                    ha="center",
                    va="bottom",
                    rotation=45,
                    fontsize=8,
                )

    ax2.set_title("Top 3 Most Frequent Profane Words by Sender")
    ax2.set_ylabel("Frequency")
    ax2.set_xticks([])

    # Add legends only if there's data
    if frequencies:
        ax2.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(right=0.85, hspace=0.3)
    return fig
