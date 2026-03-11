from domains.value_objects.zip_code import ZipCode
from domains.exceptions import (
    ZipCodeError,
    ZipCodeInvalidTypeError,
    ZipCodeInvalidFormatError,
)
import re
import pytest


# ------------------------------
# Creation tests
# ------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [
        ("12345-678", "12345678"),
        ("12345678", "12345678"),
        ("123456789", "12345678"),
        ("12345-6789", "12345678"),
        ("123456789", "12345678"),
    ],
)
def test_zip_code_normalization(value, expected):
    zip_code = ZipCode(value)
    assert zip_code.value == expected


@pytest.mark.parametrize(
    "value",
    [
        12345678,
        None,
        "1234",
        "123456789",
        "abcdefgh",
    ],
)
def test_invalid_zip_code_raises_exception(value):
    with pytest.raises(ZipCodeError):
        ZipCode(value)


# ------------------------------
# Normalization tests
# ------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [
        ("12345-678", "12345678"),
        ("12345678", "12345678"),
        ("12345678", "12345678"),
        ("12345-678", "12345678"),
        ("12345678", "12345678"),
    ],
)
def test_zip_code_normalization(value, expected):
    zip_code = ZipCode(value)
    assert zip_code.value == expected


# ------------------------------
# Exception tests
# ------------------------------

@pytest.mark.parametrize(
    "value, exception",
    [
        (12345678, ZipCodeInvalidTypeError),
        (None, ZipCodeInvalidTypeError),
        ("1234", ZipCodeInvalidFormatError),
        ("123456789", ZipCodeInvalidFormatError),
        ("abcdefgh", ZipCodeInvalidFormatError),
    ],
)
def test_invalid_zip_code_raises_exception(value, exception):
    with pytest.raises(exception):
        ZipCode(value)


# ------------------------------
# is_valid tests
# ------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [
        ("12345-678", True),
        ("12345678", True),
        ("12345678", True),
        ("12345-678", True),
        ("12345678", True),
        ("1234", False),
        ("1234567890", False),
        ("abcdefgh", False),
        (12345678, False),
        (None, False),
    ],
)
def test_zip_code_is_valid(value, expected):
    assert ZipCode.is_valid(value) is expected


# ------------------------------
# Equality tests
# ------------------------------

def test_zip_code_equality():
    zip_code1 = ZipCode("12345-678")
    zip_code2 = ZipCode("12345678")
    zip_code3 = ZipCode("87654-321")

    assert zip_code1 == zip_code2
    assert zip_code1 != zip_code3
    assert zip_code2 != zip_code3


# ------------------------------
# Hash tests
# ------------------------------

def test_zip_code_hash():
    zip_code1 = ZipCode("12345-678")
    zip_code2 = ZipCode("12345678")
    zip_code3 = ZipCode("87654-321")

    assert hash(zip_code1) == hash(zip_code2)
    assert hash(zip_code1) != hash(zip_code3)

def test_zip_code_as_dict_key():
    zip_code1 = ZipCode("12345-678")
    zip_code2 = ZipCode("12345678")
    zip_code3 = ZipCode("87654-321")

    zip_code_dict = {
        zip_code1: "Address 1",
        zip_code3: "Address 2",
    }

    assert zip_code_dict[zip_code1] == "Address 1"
    assert zip_code_dict[zip_code2] == "Address 1"
    assert zip_code_dict[zip_code3] == "Address 2"


# ------------------------------
# Representation tests
# -------------------------------

def test_zip_code_representation():
    zip_code = ZipCode("12345-678")
    repr_str = repr(zip_code)

    assert repr_str == "ZipCode('12345-678')"
    assert str(zip_code) == "12345-678"


# ------------------------------
# Immutability tests
# ------------------------------

def test_zip_code_is_immutable():
    zip_code = ZipCode("12345-678")

    with pytest.raises(ZipCodeError):
        zip_code.value = "87654-321"

    with pytest.raises(ZipCodeError):
        zip_code.formatted = "87654321"