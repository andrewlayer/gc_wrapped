from typing import Dict, List
from collections import defaultdict, Counter
from helpers.db import Message

reaction_words = ["liked", "loved", "disliked", "laughed", "emphasized", "questioned"]

def react_frequency(messages: list[Message]):
    results = defaultdict(lambda: {"frequency": 0, "reaction_frequency": Counter()})

    for message in messages:
        if not message.text:
            continue

        words = message.text.lower().split()
        # TODO: account for person typing loved, liked, etc before a non react message
        if words[0] in reaction_words:
            sender = message.sender_name
            results[sender]["frequency"] += 1
            results[sender]["reaction_frequency"].update({words[0]: 1})

    return {
        sender: {
            "frequency": data["frequency"],
            "reaction_frequency": dict(data["reaction_frequency"]),
        }
        for sender, data in results.items()
    }