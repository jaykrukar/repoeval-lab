"""Independent behavioral tests for the HTTP Retry-After challenge."""

from datetime import datetime, timezone
import pytest

from retry_after import retry_after_seconds


NOW = datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)


@pytest.mark.parametrize("value, expected", [("0", 0), ("12", 12), (" 007 ", 7), ("9" * 80, 10**80 - 1)])
def test_delay_seconds(value, expected):
    assert retry_after_seconds(value, NOW) == expected


def test_future_http_date_rounds_up():
    assert retry_after_seconds("Fri, 02 Jan 2026 03:04:06 GMT", NOW) == 1


def test_past_http_date_clamps_to_zero():
    assert retry_after_seconds("Fri, 02 Jan 2026 03:04:04 GMT", NOW) == 0


@pytest.mark.parametrize("value", [
    "Friday, 02-Jan-26 03:04:06 GMT",  # obsolete RFC 850 form
    "Fri Jan  2 03:04:06 2026",         # obsolete asctime form
])
def test_supported_http_date_forms(value):
    assert retry_after_seconds(value, NOW) == 1


@pytest.mark.parametrize("value", ["", "-1", "+1", "1.5", "1, 2", "tomorrow", "2026-01-02T03:04:06Z"])
def test_rejects_invalid_field_values(value):
    with pytest.raises(ValueError):
        retry_after_seconds(value, NOW)


@pytest.mark.parametrize("value", [None, 5, True])
def test_rejects_non_string_values(value):
    with pytest.raises(ValueError):
        retry_after_seconds(value, NOW)


def test_rejects_naive_now():
    with pytest.raises(ValueError, match="timezone-aware"):
        retry_after_seconds("Fri, 02 Jan 2026 03:04:06 GMT", datetime(2026, 1, 2))


def test_rejects_date_without_timezone():
    with pytest.raises(ValueError):
        retry_after_seconds("Fri, 02 Jan 2026 03:04:06 -0000", NOW)
