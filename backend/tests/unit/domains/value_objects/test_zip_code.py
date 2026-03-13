from domains.value_objects.zip_code import ZipCode
from domains.exceptions import (
    ZipCodeError,
    ZipCodeInvalidTypeError,
    ZipCodeInvalidFormatError,
)
import pytest


VALID_ZIP = "12345-678"
VALID_ZIP_NORMALIZED = "12345678"
VALID_ZIP_2 = "87654-321"
VALID_ZIP_NORMALIZED_2 = "87654321"


# ----------------------------------------
# Testes de criação e validação
# ----------------------------------------

def test_create_valid_zip_code():
    zip_code = ZipCode(VALID_ZIP)

    assert zip_code.value == VALID_ZIP_NORMALIZED
    assert zip_code.formatted == VALID_ZIP


def test_create_valid_zip_code_without_dash():
    zip_code = ZipCode("12345678")

    assert zip_code.value == VALID_ZIP_NORMALIZED
    assert zip_code.formatted == VALID_ZIP


def test_create_zip_code_with_invalid_type():
    with pytest.raises(ZipCodeInvalidTypeError):
        ZipCode(12345678)


# ----------------------------------------
# Testes de normalização
# ----------------------------------------

@pytest.mark.parametrize(
    "value,expected",
    [
        ("12345-678", "12345678"),
        ("12345678", "12345678"),
        ("12345 678", "12345678"),
        ("12345.678", "12345678"),
    ],
)
def test_zip_code_normalization(value, expected):
    zip_code = ZipCode(value)

    assert zip_code.value == expected


# ----------------------------------------
# Testes de exceções
# ----------------------------------------

@pytest.mark.parametrize(
    "value,exception",
    [
        (None, ZipCodeInvalidTypeError),
        (12345678, ZipCodeInvalidTypeError),
        ("1234", ZipCodeInvalidFormatError),
        ("1234567", ZipCodeInvalidFormatError),
        ("123456789", ZipCodeInvalidFormatError),
        ("abcdefgh", ZipCodeInvalidFormatError),
    ],
)
def test_invalid_zip_code_raises_exception(value, exception):
    with pytest.raises(exception):
        ZipCode(value)


# ----------------------------------------
# Testes de validação pública
# ----------------------------------------

@pytest.mark.parametrize(
    "value,expected",
    [
        ("12345-678", True),
        ("12345678", True),
        ("12345 678", True),
        ("1234", False),
        ("123456789", False),
        ("abcdefgh", False),
        (None, False),
        (12345678, False),
    ],
)
def test_is_valid_zip_code(value, expected):
    assert ZipCode.is_valid(value) is expected


# ----------------------------------------
# Testes de igualdade
# ----------------------------------------

def test_zip_code_equality():
    zip1 = ZipCode(VALID_ZIP)
    zip2 = ZipCode(VALID_ZIP_NORMALIZED)
    zip3 = ZipCode(VALID_ZIP_2)

    assert zip1 == zip2
    assert zip1 != zip3


# ----------------------------------------
# Testes de hash
# ----------------------------------------

def test_zip_code_hash():
    zip1 = ZipCode(VALID_ZIP)
    zip2 = ZipCode(VALID_ZIP_NORMALIZED)
    zip3 = ZipCode(VALID_ZIP_2)

    assert hash(zip1) == hash(zip2)
    assert hash(zip1) != hash(zip3)


def test_zip_code_as_dict_key():
    zip_codes = {
        ZipCode(VALID_ZIP): "Address 1",
        ZipCode(VALID_ZIP_2): "Address 2",
    }

    assert zip_codes[ZipCode(VALID_ZIP_NORMALIZED)] == "Address 1"


# ----------------------------------------
# Testes de representação
# ----------------------------------------

def test_str_returns_formatted():
    zip_code = ZipCode(VALID_ZIP)

    assert str(zip_code) == VALID_ZIP


def test_repr_contains_class_name():
    zip_code = ZipCode(VALID_ZIP)

    representation = repr(zip_code)

    assert "ZipCode(" in representation
    assert VALID_ZIP in representation


# ----------------------------------------
# Teste de imutabilidade
# ----------------------------------------

def test_zip_code_is_immutable():
    zip_code = ZipCode(VALID_ZIP)

    with pytest.raises(ZipCodeError):
        zip_code.value = "87654321"

    with pytest.raises(ZipCodeError):
        zip_code.formatted = "87654-321"