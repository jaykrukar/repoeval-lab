import re


def normalize_tag(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    normalized = re.sub(r"[\s_]+", "-", value.strip().lower())
    normalized = re.sub(r"[^a-z0-9-]", "", normalized)
    normalized = re.sub(r"-+", "-", normalized)
    return normalized.strip("-")
