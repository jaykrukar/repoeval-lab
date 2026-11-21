def normalize_tag(value: str) -> str:
    """Normalize a short tag. Replace this starter implementation."""
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    return value.strip().lower()
