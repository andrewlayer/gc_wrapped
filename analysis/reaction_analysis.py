from typing import Dict, List
from collections import defaultdict, Counter
from helpers.db import Message
from analysis import timeseries_analysis

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

def get_message_total(messages: list[Message]):
    results = defaultdict(lambda: {"count": 0})

    for message in messages:
        sender = message.sender_name
        results[sender]['count'] += 1

    return { 
        sender: data['count']
        for sender, data in results.items()
    } 

def get_react_percentage( messages: List[Message]):
    message_count = get_message_total(messages)
    react_count = react_frequency(messages)

    return {
        sender: round((react_count[sender]['frequency'] / message_count[sender])*100, 2)
        for sender in message_count.keys()
    }
