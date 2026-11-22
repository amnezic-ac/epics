import pytest
from src.backend.parameters import Cutype

@pytest.mark.parametrize("value", [
    "INDIVIDUAL",
    "GROUP",
    "RESOURCE",
    "ROOM",
    "UNKNOWN"
])
def test_valid_known_value(value: str):
    assert str(Cutype(value)) == f"CUTYPE={value.strip().upper()}"

@pytest.mark.parametrize("value", [
    "individual",
    "group",
    "resource",
    "room",
    "unknown"
])
def test_valid_known_values_lowercase(value: str):
    assert str(Cutype(value)) == f"CUTYPE={value.strip().upper()}"

@pytest.mark.parametrize("value", [
    "iNdivIdual",
    "gROUP",
    "RESOurce",
    "rOOm",
    "unknown"
])
def test_valid_known_values_random_cases(value: str):
    assert str(Cutype(value)) == f"CUTYPE={value.strip().upper()}"