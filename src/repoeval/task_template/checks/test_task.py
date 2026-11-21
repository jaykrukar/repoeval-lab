import pytest

from tag_normalizer import normalize_tag


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("Red Fox", "red-fox"),
        ("  Red__Fox  ", "red-fox"),
        ("tabs\tand\nlines", "tabs-and-lines"),
        ("---leading and trailing---", "leading-and-trailing"),
        ("many---hyphens", "many-hyphens"),
        ("A...B", "ab"),
        ("tag_42", "tag-42"),
        ("MiXeD", "mixed"),
        ("Cafe", "cafe"),
        ("Crème brûlée", "crme-brle"),
        ("東京", ""),
        ("---", ""),
        ("", ""),
    ],
)
def test_normalize_tag_examples(value, expected):
    assert normalize_tag(value) == expected


@pytest.mark.parametrize("value", [None, 4, [], {}])
def test_non_strings_raise_type_error(value):
    with pytest.raises(TypeError):
        normalize_tag(value)


def test_does_not_mutate_input():
    value = " Mixed__Tag "
    normalize_tag(value)
    assert value == " Mixed__Tag "
