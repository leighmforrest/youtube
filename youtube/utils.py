import isodate
from datetime import datetime, timedelta, timezone


one_day_ago = lambda: datetime.now(tz=timezone.utc) - timedelta(hours=24)


def chunk_list(lyst, chunk_size=50):
    """Split a list into chunks of chunk_size. The default is 50."""
    return [lyst[i : i + chunk_size] for i in range(0, len(lyst), chunk_size)]


def get_total_seconds(duration_string):
    """Get the integer duration in seconds from an ISO 8601 duration string."""
    duration = isodate.parse_duration(duration_string)
    total_seconds = int(duration.total_seconds())

    return total_seconds
