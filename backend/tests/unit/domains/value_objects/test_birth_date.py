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

DATE_2 = date(2000, 1, 1)
DATE_2_STR_BR = "01/01/2000"
DATE_2_STR_ISO = "2000-01-01"

DATE_3 = date(1950, 12, 31)
DATE_3_STR_BR = "31/12/1950"
DATE_3_STR_ISO = "1950-12-31"


def calculate_age(birth: date) -> int:
    today = date.today()
    age = today.year - birth.year
    if (today.month, today.day) < (birth.month, birth.day):
        age -= 1
    return age


# ----------------------------------------
# Testes de criação e validação
# ----------------------------------------

def test_create_valid_birth_date():
    bd = BirthDate(DATE_1)

    assert bd.value == DATE_1
    assert bd.year == 1990
    assert bd.month == 5
    assert bd.day == 15
    assert bd.formatted_br == DATE_1_STR_BR
    assert bd.formatted_us == DATE_1_STR_ISO
    assert bd.age == calculate_age(DATE_1)


@pytest.mark.parametrize(
    "value,expected_date",
    [
        (DATE_1_STR_BR, DATE_1),
        (DATE_1_STR_ISO, DATE_1),
        (DATE_2_STR_BR, DATE_2),
        (DATE_2_STR_ISO, DATE_2),
        (DATE_3_STR_BR, DATE_3),
        (DATE_3_STR_ISO, DATE_3),
    ],
)
def test_create_birth_date_from_strings(value, expected_date):
    bd = BirthDate(value)

    assert bd.value == expected_date


# ----------------------------------------
# Testes de exceções
# ----------------------------------------

@pytest.mark.parametrize(
    "value,exception",
    [
        (date.today() + timedelta(days=1), BirthDateInFutureError),
        (date(1800, 1, 1), BirthDateTooOldError),
        ("12-31-1950", BirthDateInvalidFormatError),
        ("32/13/1950", BirthDateInvalidValueError),
        (123, BirthDateInvalidTypeError),
        (["1990", "05", "15"], BirthDateInvalidTypeError),
    ],
)
def test_invalid_birth_date_raises_exception(value, exception):
    with pytest.raises(exception):
        BirthDate(value)


# ----------------------------------------
# Testes de is_valid
# ----------------------------------------

@pytest.mark.parametrize(
    "value,expected",
    [
        (DATE_1, True),
        (DATE_1_STR_BR, True),
        (DATE_1_STR_ISO, True),
        (date.today(), True),
        (date.today() + timedelta(days=1), False),
        (date(1800, 1, 1), False),
        ("12-31-1950", False),
        ("32/13/1950", False),
        (123, False),
    ],
)
def test_birth_date_is_valid(value, expected):
    assert BirthDate.is_valid(value) is expected


# ----------------------------------------
# Testes de propriedades
# ----------------------------------------

def test_birth_date_properties():
    bd = BirthDate(DATE_1)

    assert bd.year == DATE_1.year
    assert bd.month == DATE_1.month
    assert bd.day == DATE_1.day
    assert bd.formatted_br == DATE_1_STR_BR
    assert bd.formatted_us == DATE_1_STR_ISO
    assert bd.age == calculate_age(DATE_1)
    assert bd.is_adult == (bd.age >= 18)


# ----------------------------------------
# Testes de igualdade
# ----------------------------------------

def test_birth_date_equality():
    bd1 = BirthDate(DATE_1)
    bd2 = BirthDate(DATE_1_STR_BR)
    bd3 = BirthDate(DATE_1_STR_ISO)

    assert bd1 == bd2
    assert bd2 == bd3


def test_birth_date_inequality():
    bd1 = BirthDate(DATE_1)
    bd2 = BirthDate(DATE_2)

    assert bd1 != bd2


# ----------------------------------------
# Teste de hash
# ----------------------------------------

def test_birth_date_hash():
    bd1 = BirthDate(DATE_1)
    bd2 = BirthDate(DATE_1_STR_BR)

    assert hash(bd1) == hash(bd2)


def test_birth_date_set_behavior():
    bd1 = BirthDate(DATE_1)
    bd2 = BirthDate(DATE_1_STR_BR)

    s = {bd1, bd2}

    assert len(s) == 1


# ----------------------------------------
# Teste de imutabilidade
# ----------------------------------------

def test_birth_date_is_immutable():
    bd = BirthDate(DATE_1)

    with pytest.raises(BirthDateError):
        bd.value = DATE_2


# ----------------------------------------
# Teste de idade e maioridade
# ----------------------------------------

def test_adult_boundary():
    today = date.today()

    birth = date(today.year - 18, today.month, today.day)

    bd = BirthDate(birth)

    assert bd.is_adult is True


# ----------------------------------------
# Teste de __str__
# ----------------------------------------

def test_str_returns_formatted():
    bd = BirthDate(DATE_1)

    assert str(bd) == DATE_1_STR_BR


# ----------------------------------------
# Teste de __repr__
# ----------------------------------------

def test_repr_contains_class_name():
    bd = BirthDate(DATE_1)

    representation = repr(bd)

    assert "BirthDate(" in representation
    assert DATE_1_STR_ISO in representation


# ----------------------------------------
# Teste property-based com Hypothesis
# ----------------------------------------
@given(st.dates(min_value=date((date.today().year - 119), 1, 1), max_value=date.today()))
def test_birth_date_never_breaks_with_random_dates(date_value):
    bd = BirthDate(date_value)

    assert isinstance(bd.value, date)
    assert isinstance(bd.year, int)
    assert isinstance(bd.month, int)
    assert isinstance(bd.day, int)
    assert isinstance(bd.formatted_br, str)
    assert isinstance(bd.formatted_us, str)
    assert isinstance(bd.age, int)


@given(st.text())
def test_random_invalid_strings(value):
    if not BirthDate.is_valid(value):
        with pytest.raises(BirthDateError):
            BirthDate(value)