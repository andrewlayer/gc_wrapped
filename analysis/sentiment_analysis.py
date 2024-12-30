from typing import Dict, List
from collections import defaultdict, Counter
from better_profanity import profanity
from helpers.db import Message


def profanity_freq(messages: list[Message]):
    profanity.load_censor_words()

    results = defaultdict(lambda: {"frequency": 0, "cuss_frequency": Counter()})

    for message in messages:
        if not message.text:
            continue

        words = message.text.lower().split()
        profane_words = [word for word in words if profanity.contains_profanity(word)]

        sender = message.sender_name
        results[sender]["frequency"] += len(profane_words)
        results[sender]["cuss_frequency"].update(profane_words)

    return {
        sender: {
            "frequency": data["frequency"],
            "cuss_frequency": dict(data["cuss_frequency"]),
        }
        for sender, data in results.items()
    }
