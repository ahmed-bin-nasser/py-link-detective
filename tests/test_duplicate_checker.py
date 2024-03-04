import pytest

from py_link_detective.detective import is_duplicate_checker


@pytest.fixture
def duplicate_checker():
    return is_duplicate_checker()


def test_is_duplicate(duplicate_checker):
    # Test for a URL that hasn't been seen before
    assert duplicate_checker("https://example.com") == False
    # Test for a duplicate URL
    assert duplicate_checker("https://example.com") == True
    # Test for another URL that hasn't been seen before
    assert duplicate_checker("https://another-example.com") == False
    # Test for the same duplicate URL again
    assert duplicate_checker("https://example.com") == True
