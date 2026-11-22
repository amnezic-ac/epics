import pytest

from src.backend.parameters import Altrep

def test_simple_valid_altrep():
    value = "__Markdown italic text__"
    altrep = Altrep(value)
    assert str(altrep) == f"ALTREP=\"{value}\""