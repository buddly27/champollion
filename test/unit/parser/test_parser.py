# :coding: utf-8

import pytest

import champollion.parser


def test_get_environment_error():
    """Raise an error if the path is incorrect."""
    with pytest.raises(OSError):
        champollion.parser.fetch_environment("")


def test_get_environment_empty(temporary_directory):
    """Return an empty environment."""
    environment = {
        "module": {},
        "class": {},
        "method": {},
        "attribute": {},
        "function": {},
        "data": {},
        "file": {}
    }
    assert champollion.parser.fetch_environment(
        temporary_directory
    ) == environment
