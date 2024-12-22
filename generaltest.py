from db import MessagesDB
from datetime import datetime, date, timedelta

# Apple's reference date (January 1, 2001)
APPLE_EPOCH = datetime(2001, 1, 1)

def apple_time_to_datetime(apple_timestamp: int) -> datetime:
    """Convert Apple's nanosecond timestamp to Python datetime"""
    seconds_since_epoch = (
        apple_timestamp / 1_000_000_000
    )  # Convert nanoseconds to seconds
    return APPLE_EPOCH + timedelta(seconds=seconds_since_epoch)

AP_SQUAD_ID = 'chat305160764389025638'

def print_first_and_last_dates():
    with MessagesDB() as db:
        messages = db.get_chat_messages(
            chat_identifier=AP_SQUAD_ID,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31)
        )
        if not messages:
            print("No messages found")
            return

        # Messages are sorted by date, latest first
        latest_message = messages[0]
        earliest_message = messages[-1]

        print(f"First message date: {earliest_message['date']:%Y-%m-%d %H:%M:%S}")
        print(f"Last message date: {latest_message['date']:%Y-%m-%d %H:%M:%S}")
        print(f"Total messages: {len(messages)}")


def print_user_message_stats():
    with MessagesDB() as db:
        full_chat_messages = db.get_chat_messages(chat_identifier=AP_SQUAD_ID)
        messages = db.get_chat_messages_by_user(full_chat_messages)

        for user, user_messages in messages.items():
            print(user, len(user_messages))
            # print(len(messages))
        
        print('End')

if __name__ == "__main__":
    print('----- First and Last message dates -----')
    print_first_and_last_dates()
    print('----- User Message Count -----')
    print_user_message_stats()
