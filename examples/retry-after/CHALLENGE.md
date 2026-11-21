# Challenge: Parse an HTTP Retry-After value

Implement `retry_after_seconds(value, now=None)` in `retry_after.py`.

- `value` is a string containing either nonnegative delay-seconds or an HTTP date.
- Accept the three HTTP-date forms recipients are required to understand.
- A delay-seconds value contains decimal digits only; whitespace around the field is allowed.
- For dates in the past, return `0`. For future dates, round up to a whole second so a caller does not retry early.
- When `now` is provided it must be a timezone-aware `datetime`; otherwise use the current UTC time.
- Reject malformed values and naive `now` values with `ValueError`.
- Do not mutate inputs or depend on third-party packages.

The verifier exercises boundary cases and accepts any implementation that follows
the contract. This original exercise is not claimed to be exclusive or unpublished.
