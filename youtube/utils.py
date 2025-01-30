from datetime import datetime, timedelta, timezone

import isodate

one_day_ago = lambda: datetime.now(tz=timezone.utc) - timedelta(hours=24)

snake_to_capitals = lambda snake_str: " ".join(
    word.capitalize() for word in snake_str.split("_")
)

add_at_symbol = lambda string: string if string.startswith("@") else "@" + string
remove_at_symbol = lambda string: string[1:] if string.startswith("@") else string


def chunk_list(lyst: list, chunk_size: int = 50) -> list:
    """Split a list into chunks of chunk_size. The default is 50."""
    return [lyst[i : i + chunk_size] for i in range(0, len(lyst), chunk_size)]


def get_total_seconds(duration_string: str) -> int:
    """Get the integer duration in seconds from an ISO 8601 duration string."""
    duration = isodate.parse_duration(duration_string)
    total_seconds = int(duration.total_seconds())

    return total_seconds
