import pytest
from ferret.cleaner.text import normalize_text, remove_special_chars


@pytest.mark.parametrize("text,expected", [
    (None, ""),
    ("\n", ""),
    ("This \n is a title", "This  is a title"),
    ("This \b is a \r title \t", "This  is a  title "),
])
def test_removal_of_special_characters(text, expected):
    actual = remove_special_chars(text)
    assert actual == expected


@pytest.mark.parametrize("text,expected", [
    (None, ""),
    (" ", ""),
    (" This is a title ", "This is a title"),
    ("This  is  a title", "This is a title"),
    ("This        is       a          title", "This is a title")
])
def test_normalize_text(text, expected):
    actual = normalize_text(text)
    assert actual == expected
