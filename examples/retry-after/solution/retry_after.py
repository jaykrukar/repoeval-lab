"""Reference implementation for the HTTP Retry-After challenge."""

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import math
import re


def retry_after_seconds(value, now=None):
    if not isinstance(value, str):
        raise ValueError("Retry-After must be a string")
    field = value.strip()
    if not field:
        raise ValueError("Retry-After must not be empty")
    if re.fullmatch(r"[0-9]+", field):
        return int(field)

    if now is None:
        now = datetime.now(timezone.utc)
    if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("now must be a timezone-aware datetime")
    try:
        target = parsedate_to_datetime(field)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("Retry-After is neither delay-seconds nor an HTTP date") from exc
    # RFC 9110's obsolete asctime form has no explicit zone; HTTP-date defines
    # it as GMT. email.utils therefore returns a naive datetime for that form.
    if target.tzinfo is None and re.fullmatch(
        r"[A-Za-z]{3} [A-Za-z]{3} {1,2}\d{1,2} "
        r"\d{2}:\d{2}:\d{2} \d{4}", field
    ):
        target = target.replace(tzinfo=timezone.utc)
    if target.tzinfo is None or target.utcoffset() is None:
        raise ValueError("HTTP date must include a timezone")
    seconds = (target - now).total_seconds()
    return max(0, math.ceil(seconds))
