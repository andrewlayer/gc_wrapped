from db import MessagesDB
from datetime import datetime, timedelta

# Apple's reference date (January 1, 2001)
APPLE_EPOCH = datetime(2001, 1, 1)


def apple_time_to_datetime(apple_timestamp: int) -> datetime:
    """Convert Apple's nanosecond timestamp to Python datetime"""
    seconds_since_epoch = (
        apple_timestamp / 1_000_000_000
    )  # Convert nanoseconds to seconds
    return APPLE_EPOCH + timedelta(seconds=seconds_since_epoch)


def main():
    with MessagesDB() as db:
        messages = db.get_chat_messages(chat_identifier="chat734857422501332926")
        if not messages:
            print("No messages found")
            return

        last_message = messages[-1]

        first_message_date = apple_time_to_datetime(messages[0][2])
        last_message_date = apple_time_to_datetime(last_message[2])

        print(f"First message date: {first_message_date:%Y-%m-%d %H:%M:%S}")
        print(f"Last message date: {last_message_date:%Y-%m-%d %H:%M:%S}")
        print(f"Total messages: {len(messages)}")


if __name__ == "__main__":
    main()
