from hypothesis import given, strategies as st
from domains.value_objects.cpf import CPF
from domains.exceptions import (
    CPFError,
    CPFInvalidLengthError,
    CPFInvalidCheckDigitsError,
    CPFRepeatedDigitsError,
    CPFInvalidTypeError,
)
import pytest


VALID_CPF = "52998224725"
VALID_CPF_FORMATTED = "529.982.247-25"
VALID_CPF_MASKED = "529.***.***-25"

VALID_CPF_2 = "16899535009"


# ----------------------------------------
# Testes de criação e validação de CPF
# ----------------------------------------

def test_create_valid_cpf():
    cpf = CPF(VALID_CPF)

    assert cpf.value == VALID_CPF
    assert cpf.formatted == VALID_CPF_FORMATTED
    assert cpf.masked == VALID_CPF_MASKED


def test_create_cpf_with_formatted_string():
    cpf = CPF("529.982.247-25")

    assert cpf.value == VALID_CPF
    assert cpf.formatted == VALID_CPF_FORMATTED


def test_create_cpf_with_invalid_type():
    with pytest.raises(CPFInvalidTypeError):
        CPF(123)


# ----------------------------------------
# Testes de validação de CPF
# ----------------------------------------

@pytest.mark.parametrize(
    "value,expected",
    [
        ("52998224725", True),
        ("529.982.247-25", True),
        ("16899535009", True),
        ("11111111111", False),
        ("00000000000", False),
        ("1234567890", False),
        ("123456789012", False),
        ("52998224724", False),
    ],
)
def test_is_valid_cpf(value, expected):
    assert CPF.is_valid(value) is expected


# ----------------------------------------
# Testes de exceções
# ----------------------------------------

@pytest.mark.parametrize(
    "value,exception",
    [
        ("11111111111", CPFRepeatedDigitsError),
        ("00000000000", CPFRepeatedDigitsError),
        ("1234567890", CPFInvalidLengthError),
        ("123456789012", CPFInvalidLengthError),
        ("52998224724", CPFInvalidCheckDigitsError),
    ],
)
def test_invalid_cpf_raises_exception(value, exception):
    with pytest.raises(exception):
        CPF(value)


# ----------------------------------------
# Testes de propriedades
# ----------------------------------------

def test_cpf_properties():
    cpf = CPF(VALID_CPF)

    assert cpf.value == VALID_CPF
    assert cpf.formatted == VALID_CPF_FORMATTED
    assert cpf.masked == VALID_CPF_MASKED


# ----------------------------------------
# Testes de igualdade
# ----------------------------------------

def test_cpf_equality():
    cpf1 = CPF(VALID_CPF)
    cpf2 = CPF("529.982.247-25")

    assert cpf1 == cpf2
    assert cpf1 == "529.982.247-25"


def test_cpf_inequality():
    cpf1 = CPF(VALID_CPF)
    cpf2 = CPF(VALID_CPF_2)

    assert cpf1 != cpf2


# ----------------------------------------
# Teste de hash
# ----------------------------------------

def test_cpf_hash():
    cpf1 = CPF(VALID_CPF)
    cpf2 = CPF("529.982.247-25")

    assert hash(cpf1) == hash(cpf2)


def test_cpf_set_behavior():
    cpf1 = CPF(VALID_CPF)
    cpf2 = CPF("529.982.247-25")

    s = {cpf1, cpf2}

    assert len(s) == 1


# ----------------------------------------
# Teste de imutabilidade
# ----------------------------------------

def test_cpf_is_immutable():
    cpf = CPF(VALID_CPF)

    with pytest.raises(CPFError):
        cpf.value = "11111111111"


# ----------------------------------------
# Teste de __str__
# ----------------------------------------

def test_str_returns_formatted():
    cpf = CPF(VALID_CPF)

    assert str(cpf) == VALID_CPF_FORMATTED


# ----------------------------------------
# Teste de __repr__
# ----------------------------------------

def test_repr_contains_class_name():
    cpf = CPF(VALID_CPF)

    representation = repr(cpf)

    assert "CPF(" in representation
    assert VALID_CPF_FORMATTED in representation


# ----------------------------------------
# Testes property-based com Hypothesis
# ----------------------------------------

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