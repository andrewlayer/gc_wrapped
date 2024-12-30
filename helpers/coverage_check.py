from calendar import c
from datetime import datetime
from helpers.db import Message


def check_message_coverage(
    messages: list[Message],
):
    """Check for messages with missing data"""

    empty_messages = sum(1 for msg in messages if msg.text is None)
    text_messages = sum(1 for msg in messages if msg.text is not None)
    total = len(messages)

    print(f"\nMessage Content Analysis:")
    print(f"Total messages: {total}")
    print(f"Messages with text: {text_messages} ({text_messages/total*100:.1f}%)")
    print(f"Messages without text: {empty_messages} ({empty_messages/total*100:.1f}%)")
