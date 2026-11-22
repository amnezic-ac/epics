from src.backend.properties.descriptive import Summary
import pytest

def test_simple_valid_summary():
    summary = Summary(
        value = "Key Note",
        altrep = None,
        language = None
    )
    assert str(summary) == "SUMMARY:Key Note"

def test_full_valid_summary():
    summary = Summary(
        value="Key Note",
        altrep="**Key Note**",
        language="en-GB"
    )
    assert str(summary) == "SUMMARY;ALTREP=\"**Key Note**\";LANGUAGE=en-GB:Key Note"

def test_invalid_language_key_summary():
    with pytest.raises(Exception):
        summary = Summary(
            value="Key Note",
            language="zz"
        )