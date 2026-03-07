import pytest
from hypothesis import given, strategies as st

from domains.value_objects.cpf import CPF
from domains.exceptions.cpf.cpf_errors import *

VALID_CPF = "52998224725"
VALID_CPF_FORMATTED = "529.982.247-25"
VALID_CPF_2 = "16899535009"


# -----------------------------
# Creation tests
# -----------------------------

def test_create_valid_cpf():
    cpf = CPF(VALID_CPF)

    assert cpf.value == VALID_CPF
    assert cpf.formatted == "529.982.247-25"
    assert cpf.masked == "529.***.***-25"


def test_create_formatted_cpf():
    cpf = CPF(VALID_CPF_FORMATTED)

    assert cpf.value == VALID_CPF
    assert cpf.formatted == VALID_CPF_FORMATTED
    assert cpf.masked == "529.***.***-25"


# -----------------------------
# Exception tests
# -----------------------------

@pytest.mark.parametrize(
    "cpf,exception",
    [
        ("11111111111", CPFRepeatedDigitsError),
        ("00000000000", CPFRepeatedDigitsError),
        ("1234567890", CPFInvalidLengthError),
        ("123456789012", CPFInvalidLengthError),
        ("52998224724", CPFInvalidCheckDigitsError),
    ],
)
def test_invalid_cpf_raises_exception(cpf, exception):
    with pytest.raises(exception):
        CPF(cpf)


# -----------------------------
# is_valid tests
# -----------------------------

@pytest.mark.parametrize(
    "value,expected",
    [
        ("52998224725", True),
        ("529.982.247-25", True),
        ("16899535009", True),
        ("11111111111", False),
        ("1234567890", False),
        ("123456789012", False),
        ("52998224724", False),
    ],
)
def test_cpf_is_valid(value, expected):
    assert CPF.is_valid(value) is expected


# -----------------------------
# Equality tests
# -----------------------------

def test_cpf_equality():
    cpf1 = CPF("52998224725")
    cpf2 = CPF("529.982.247-25")
    cpf3 = CPF(VALID_CPF_2)

    assert cpf1 == cpf2
    assert cpf1 != cpf3

    assert cpf1 == "529.982.247-25"


# -----------------------------
# Hash tests
# -----------------------------

def test_cpf_hash():
    cpf1 = CPF("52998224725")
    cpf2 = CPF("529.982.247-25")
    cpf3 = CPF(VALID_CPF_2)

    assert hash(cpf1) == hash(cpf2)
    assert hash(cpf1) != hash(cpf3)


# -----------------------------
# Immutability tests
# -----------------------------

def test_cpf_is_immutable():
    cpf = CPF(VALID_CPF)

    with pytest.raises(AttributeError):
        cpf.value = "11111111111"


def test_cpf_properties_are_stable():
    cpf = CPF(VALID_CPF)

    assert cpf.value == VALID_CPF
    assert cpf.formatted == "529.982.247-25"
    assert cpf.masked == "529.***.***-25"

    assert cpf.value == VALID_CPF
    assert cpf.formatted == "529.982.247-25"


# -----------------------------
# Property-based tests
# -----------------------------

@given(st.integers(min_value=0, max_value=9))
def test_repeated_digits_are_always_invalid(digit):
    cpf = str(digit) * 11
    assert not CPF.is_valid(cpf)
    with pytest.raises(CPFRepeatedDigitsError):
        CPF(cpf)


@given(st.text(min_size=1, max_size=20))
def test_random_invalid_values_raise_exception(value):
    if not CPF.is_valid(value):
        with pytest.raises(CPFError):
            CPF(value)