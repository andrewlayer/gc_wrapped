from datetime import datetime, timedelta
import json


def apple_time_to_datetime(apple_timestamp: int) -> datetime:
    """
    Convert Apple's nanosecond timestamp to Python datetime
    """
    APPLE_EPOCH = datetime(2001, 1, 1)
    seconds_since_epoch = apple_timestamp / 1_000_000_000  # ns to seconds
    return APPLE_EPOCH + timedelta(seconds=seconds_since_epoch)


def load_contact_map(file_path: str) -> dict:
    """
    Load JSON file mapping phone numbers/emails to names
    """
    with open(file_path, "r") as f:
        return json.load(f)


def get_contact_name(sender_id: str, contact_map: dict) -> str:
    """
    Look up the plain-text name for a given phone number/email
    """
    for name, identifiers in contact_map.items():
        if sender_id in identifiers:
            return name
    return sender_id
