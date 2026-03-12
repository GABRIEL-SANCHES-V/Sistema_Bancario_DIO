from hypothesis import given, strategies as st
from domains.value_objects.birth_date import BirthDate
from datetime import date, timedelta
from domains.exceptions import (
    BirthDateError,
    BirthDateInFutureError,
    BirthDateTooOldError,
    BirthDateInvalidTypeError,
    BirthDateInvalidFormatError,
    BirthDateInvalidValueError,
)
import pytest


DATE_1 = date(1990, 5, 15)
DATE_1_STR_BR = "15/05/1990"
DATE_1_STR_ISO = "1990-05-15"
AGE_1 = date.today().year - DATE_1.year - ((date.today().month, date.today().day) < (DATE_1.month, DATE_1.day))

DATE_2 = date(2000, 1, 1)
DATE_2_STR_BR = "01/01/2000"
DATE_2_STR_ISO = "2000-01-01"
AGE_2 = date.today().year - DATE_2.year - ((date.today().month, date.today().day) < (DATE_2.month, DATE_2.day))

DATE_3 = date(1950, 12, 31)
DATE_3_STR_BR = "31/12/1950"
DATE_3_STR_ISO = "1950-12-31"
AGE_3 = date.today().year - DATE_3.year - ((date.today().month, date.today().day) < (DATE_3.month, DATE_3.day))


# -----------------------------
# Creation tests
# -----------------------------
def test_create_valid_birth_date():
    bd1 = BirthDate(DATE_1)
    assert bd1.value == DATE_1
    assert bd1.formatted_br == DATE_1_STR_BR
    assert bd1.formatted_us == DATE_1_STR_ISO
    assert bd1.age == AGE_1

    bd2 = BirthDate(DATE_2_STR_BR)
    assert bd2.value == DATE_2
    assert bd2.formatted_br == DATE_2_STR_BR
    assert bd2.formatted_us == DATE_2_STR_ISO
    assert bd2.age == AGE_2

    bd3 = BirthDate(DATE_3_STR_ISO)
    assert bd3.value == DATE_3
    assert bd3.formatted_br == DATE_3_STR_BR
    assert bd3.formatted_us == DATE_3_STR_ISO
    assert bd3.age == AGE_3


# -----------------------------
# Exception tests
# -----------------------------

@pytest.mark.parametrize(
    "value,exception",
    [
        (date.today() + timedelta(days=1), BirthDateInFutureError),
        (date(1800, 1, 1), BirthDateTooOldError),
        ("12-31-1950", BirthDateInvalidFormatError),
        (12345, BirthDateInvalidTypeError),
        ("32/13/1950", BirthDateInvalidValueError),
    ],
)
def test_invalid_birth_date_raises_exception(value, exception):
    with pytest.raises(exception):
        BirthDate(value)


# -----------------------------
# is_valid tests
# -----------------------------

@pytest.mark.parametrize(
    "value,expected",
    [
        (DATE_1, True),
        (DATE_2, True),
        (DATE_3, True),
        (DATE_1_STR_BR, True),
        (DATE_2_STR_BR, True),
        (DATE_3_STR_BR, True),
        (DATE_1_STR_ISO, True),
        (DATE_2_STR_ISO, True),
        (DATE_3_STR_ISO, True),
        (date.today(), True),
        (date.today() + timedelta(days=1), False),
        (date(1800, 1, 1), False),
        ("12-31-1950", False),
        (12345, False),
        ("32/13/1950", False),
    ],
)
def test_birth_date_is_valid(value, expected):
    assert BirthDate.is_valid(value) is expected


# -----------------------------
# Equality tests
# -----------------------------

def test_birth_date_equality():
    bd1 = BirthDate(DATE_1)
    bd2 = BirthDate(DATE_1_STR_BR)
    bd3 = BirthDate(DATE_1_STR_ISO)
    bd4 = BirthDate(DATE_2)

    assert bd1 == bd2 == bd3
    assert bd1 != bd4


# -----------------------------
# Hash tests
# -----------------------------

def test_birth_date_hash():
    bd1 = BirthDate(DATE_1)
    bd2 = BirthDate(DATE_1_STR_BR)
    bd3 = BirthDate(DATE_2)

    assert hash(bd1) == hash(bd2)
    assert hash(bd1) != hash(bd3)

def test_birth_date_set_behavior():
    bd1 = BirthDate(DATE_1)
    bd2 = BirthDate(DATE_1_STR_BR)

    s = {bd1, bd2}

    assert len(s) == 1


# ------------------------------
# Immutability tests
# ------------------------------

def test_birth_date_is_immutable():
    bd = BirthDate(DATE_1)

    with pytest.raises(BirthDateError):
        bd.value = DATE_2


#------------------------------
# Invalid type tests
#------------------------------

def test_birth_date_invalid_type():
    with pytest.raises(BirthDateInvalidTypeError):
        BirthDate([1990, 5, 15])

    with pytest.raises(BirthDateInvalidTypeError):
        BirthDate(123)

    with pytest.raises(BirthDateInvalidTypeError):
        BirthDate({"year": 1990, "month": 5, "day": 15})


#------------------------------
# Property tests
#------------------------------

@given(st.dates(min_value=date(1900, 1, 1), max_value=date.today()))
def test_birth_date_properties(date_value):
    if not BirthDate.is_valid(date_value):
        with pytest.raises(BirthDateError):
            BirthDate(date_value)
    else:
        bd = BirthDate(date_value)

        assert bd.value == date_value
        assert bd.year == date_value.year
        assert bd.month == date_value.month
        assert bd.day == date_value.day
        assert bd.formatted_br == date_value.strftime("%d/%m/%Y")
        assert bd.formatted_us == date_value.strftime("%Y-%m-%d")
        expected_age = date.today().year - date_value.year - ((date.today().month, date.today().day) < (date_value.month, date_value.day))
        assert bd.age == expected_age
        assert bd.is_adult == (expected_age >= 18)

@given(st.text())
def test_random_strings(value):
    if not BirthDate.is_valid(value):
        with pytest.raises(BirthDateError):
            BirthDate(value)


#------------------------------
# Age tests
#------------------------------

def test_adult_boundary():
    today = date.today()

    birth = date(today.year - 18, today.month, today.day)

    bd = BirthDate(birth)

    assert bd.is_adult is True


#------------------------------
# Representation tests
#------------------------------

def test_birth_date_representation():
    bd = BirthDate(DATE_1)
    assert repr(bd) == f"BirthDate({DATE_1_STR_ISO})"
    assert str(bd) == DATE_1_STR_BR
