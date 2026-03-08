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

VALID_PHONE_NUMBER = "(11) 91234-5678"
VALID_PHONE_NUMBER_NORMALIZED = "11912345678"
VALID_PHONE_NUMBER_MASKED = "(11) *****-5678"

VALID_PHONE_NUMBER_2 = "(21) 99876-5432"
VALID_PHONE_NUMBER_NORMALIZED_2 = "21998765432"
VALID_PHONE_NUMBER_MASKED_2 = "(21) *****-5432"

# -----------------------------
# Creation tests
# -----------------------------

def test_create_valid_phone_number():
    phone_number = PhoneNumber(VALID_PHONE_NUMBER)

    assert phone_number.value == VALID_PHONE_NUMBER_NORMALIZED
    assert phone_number.formatted == VALID_PHONE_NUMBER
    assert phone_number.masked == VALID_PHONE_NUMBER_MASKED

    with pytest.raises(PhoneNumberInvalidTypeError):
        PhoneNumber(123)


#------------------------------
# Normalization tests
#------------------------------

def test_phone_number_normalization():
    phone = PhoneNumber("11 91234-5678")

    assert phone.value == "11912345678"
    assert phone.formatted == "(11) 91234-5678"


# -----------------------------
# Exception tests
# -----------------------------

@pytest.mark.parametrize(
    "phone_number,exception",
    [
        ("1191234567", PhoneNumberInvalidLengthError),
        ("119123456789", PhoneNumberInvalidLengthError),
        ("11612345678", PhoneNumberMissingDigitError),
        ("09923456788", PhoneNumberInvalidDDDError),
    ],
)
def test_invalid_phone_number_raises_exception(phone_number, exception):
    with pytest.raises(exception):
        PhoneNumber(phone_number)


#-----------------------------
# is_valid tests
#-----------------------------

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
def test_phone_number_is_valid(value, expected):
    assert PhoneNumber.is_valid(value) is expected


#-----------------------------
# Equality tests
#-----------------------------

def test_phone_number_equality():
    phone_number1 = PhoneNumber(VALID_PHONE_NUMBER)
    phone_number2 = PhoneNumber(VALID_PHONE_NUMBER_NORMALIZED)
    phone_number3 = PhoneNumber(VALID_PHONE_NUMBER_2)

    assert phone_number1 == phone_number2
    assert phone_number1 != phone_number3

def test_phone_number_equals_string():
    phone = PhoneNumber("(11) 91234-5678")

    assert phone == "11912345678"


#-----------------------------
# Hash tests
#-----------------------------

def test_phone_number_hash():
    phone_number1 = PhoneNumber(VALID_PHONE_NUMBER)
    phone_number2 = PhoneNumber(VALID_PHONE_NUMBER_NORMALIZED)
    phone_number3 = PhoneNumber(VALID_PHONE_NUMBER_2)

    assert hash(phone_number1) == hash(phone_number2)
    assert hash(phone_number1) != hash(phone_number3)


#-----------------------------
# Immutability tests
#-----------------------------

def test_phone_number_is_immutable():
    phone_number = PhoneNumber(VALID_PHONE_NUMBER)

    with pytest.raises(PhoneNumberError):
        phone_number.value = "11912345678"


#-----------------------------
# Representation tests
#-----------------------------

def test_phone_number_str():
    phone_number = PhoneNumber(VALID_PHONE_NUMBER)

    assert str(phone_number) == VALID_PHONE_NUMBER


def test_phone_number_repr():
    phone_number = PhoneNumber(VALID_PHONE_NUMBER)

    assert repr(phone_number) == "PhoneNumber('(11) 91234-5678')"


#-----------------------------
# Property-based tests
#-----------------------------

@given(value=st.from_regex(r"[0-9\(\)\-\s]+"))
def test_phone_number_is_valid_with_random_strings(value):
    if len(value) == 11 and value[2] == '9' and value[:2] in VALID_DDDS:
        assert PhoneNumber.is_valid(value) is True
    else:
        assert PhoneNumber.is_valid(value) is False
        with pytest.raises(PhoneNumberError):
            PhoneNumber(value)


@given(
    ddd=st.sampled_from(list(VALID_DDDS)),
    number=st.integers(min_value=900000000, max_value=999999999),
)
def test_generated_valid_phone_numbers(ddd, number):
    phone = f"{ddd}{number}"

    assert PhoneNumber.is_valid(phone) is True