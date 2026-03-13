from hypothesis import given, strategies as st
from domains.value_objects.phone_number import PhoneNumber, VALID_DDDS
from domains.exceptions import (
    PhoneNumberError,
    PhoneNumberInvalidLengthError,
    PhoneNumberInvalidTypeError,
    PhoneNumberMissingDigitError,
    PhoneNumberInvalidDDDError,
)
import pytest


VALID_PHONE = "(11) 91234-5678"
VALID_PHONE_NORMALIZED = "11912345678"
VALID_PHONE_MASKED = "(11) *****-5678"

VALID_PHONE_2 = "(21) 99876-5432"
VALID_PHONE_NORMALIZED_2 = "21998765432"


# ----------------------------------------
# Testes de criação e validação
# ----------------------------------------

def test_create_valid_phone_number():
    phone = PhoneNumber(VALID_PHONE)

    assert phone.value == VALID_PHONE_NORMALIZED
    assert phone.formatted == VALID_PHONE
    assert phone.masked == VALID_PHONE_MASKED
    assert phone.ddd == "11"
    assert phone.number == "912345678"


def test_create_phone_number_with_invalid_type():
    with pytest.raises(PhoneNumberInvalidTypeError):
        PhoneNumber(123)


# ----------------------------------------
# Testes de normalização
# ----------------------------------------

def test_phone_number_normalization():
    phone = PhoneNumber("11 91234-5678")

    assert phone.value == VALID_PHONE_NORMALIZED
    assert phone.formatted == VALID_PHONE


# ----------------------------------------
# Testes de exceções
# ----------------------------------------

@pytest.mark.parametrize(
    "value,exception",
    [
        ("1191234567", PhoneNumberInvalidLengthError),
        ("119123456789", PhoneNumberInvalidLengthError),
        ("11612345678", PhoneNumberMissingDigitError),
        ("09923456788", PhoneNumberInvalidDDDError),
    ],
)
def test_invalid_phone_numbers(value, exception):
    with pytest.raises(exception):
        PhoneNumber(value)


# ----------------------------------------
# Testes de validação pública
# ----------------------------------------

@pytest.mark.parametrize(
    "value,expected",
    [
        ("(11) 91234-5678", True),
        ("(21) 99876-5432", True),
        ("1191234567", False),
        ("119123456789", False),
        ("11812345678", False),
        ("1112345678", False),
    ],
)
def test_is_valid_phone_number(value, expected):
    assert PhoneNumber.is_valid(value) is expected


# ----------------------------------------
# Testes de igualdade
# ----------------------------------------

def test_phone_number_equality():
    phone1 = PhoneNumber(VALID_PHONE)
    phone2 = PhoneNumber(VALID_PHONE_NORMALIZED)
    phone3 = PhoneNumber(VALID_PHONE_2)

    assert phone1 == phone2
    assert phone1 != phone3


def test_phone_number_equals_string():
    phone = PhoneNumber(VALID_PHONE)

    assert phone == VALID_PHONE_NORMALIZED


# ----------------------------------------
# Testes de hash
# ----------------------------------------

def test_phone_number_hash():
    phone1 = PhoneNumber(VALID_PHONE)
    phone2 = PhoneNumber(VALID_PHONE_NORMALIZED)
    phone3 = PhoneNumber(VALID_PHONE_2)

    assert hash(phone1) == hash(phone2)
    assert hash(phone1) != hash(phone3)


# ----------------------------------------
# Teste de imutabilidade
# ----------------------------------------

def test_phone_number_is_immutable():
    phone = PhoneNumber(VALID_PHONE)

    with pytest.raises(PhoneNumberError):
        phone.value = "11912345678"


# ----------------------------------------
# Testes de representação
# ----------------------------------------

def test_str_returns_formatted():
    phone = PhoneNumber(VALID_PHONE)

    assert str(phone) == VALID_PHONE


def test_repr_contains_class_name():
    phone = PhoneNumber(VALID_PHONE)

    representation = repr(phone)

    assert "PhoneNumber(" in representation
    assert VALID_PHONE in representation


# ----------------------------------------
# Property-based tests com Hypothesis
# ----------------------------------------

@given(
    ddd=st.sampled_from(list(VALID_DDDS)),
    number=st.integers(min_value=900000000, max_value=999999999),
)
def test_generated_valid_phone_numbers(ddd, number):
    value = f"{ddd}{number}"

    phone = PhoneNumber(value)

    assert phone.ddd == ddd
    assert phone.number == str(number)
    assert PhoneNumber.is_valid(value) is True


@given(st.text())
def test_phone_number_never_breaks_with_random_strings(value):
    try:
        phone = PhoneNumber(value)

        assert isinstance(phone.value, str)
        assert isinstance(phone.formatted, str)
        assert isinstance(phone.masked, str)
        assert isinstance(phone.ddd, str)
        assert isinstance(phone.number, str)

    except PhoneNumberError:
        assert PhoneNumber.is_valid(value) is False