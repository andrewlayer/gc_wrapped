from datetime import datetime, timedelta
import json
import os
from pathlib import Path
import tempfile

from matplotlib import pyplot as plt


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


def figure_to_tempfile(fig: plt.Figure) -> Path:
    """
    Save a matplotlib figure to a temporary file and return the path
    Args:
        fig: matplotlib figure object
    Returns:
        Path: path to saved image file
    """
    temp_dir = Path(tempfile.gettempdir()) / "gc_wrapped"
    temp_dir.mkdir(exist_ok=True)

    # Generate unique filename
    temp_file = temp_dir / f"timeseries_{os.urandom(4).hex()}.png"

    fig.savefig(temp_file, dpi=300, bbox_inches="tight", transparent=True, format="png")
    plt.close(fig)
    return temp_file
