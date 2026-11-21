# Normalize a tag

Implement `normalize_tag(value: str) -> str` in `tag_normalizer.py`.

## Contract

- Accept a string. Raise `TypeError` for every non-string input.
- Trim whitespace from both ends and convert ASCII uppercase letters to lowercase.
- Replace each consecutive run of whitespace or underscores with one hyphen.
- Remove every character except ASCII lowercase letters, digits, and hyphens.
- Collapse consecutive hyphens to one and remove hyphens at the beginning and end.
- Return an empty string when no allowed characters remain.
- Do not modify the input value.

## Examples

| Input | Output |
|---|---|
| `"  Red__Fox  "` | `"red-fox"` |
| `"A...B"` | `"ab"` |
| `"---"` | `""` |
| `"Cafe"` | `"cafe"` |

The verifier checks the documented behavior, not a particular algorithm. Implementations that meet the contract should pass.
