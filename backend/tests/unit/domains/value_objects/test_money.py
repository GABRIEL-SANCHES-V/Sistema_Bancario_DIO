from decimal import Decimal
from domains.value_objects.money import Money
from domains.exceptions import (
    MoneyError,
    MoneyInvalidTypeError,
    MoneyInvalidValueError,
)
from hypothesis import given, strategies as st
import pytest


# ----------------------------------------
# Testes de criação e validação de Money
# ----------------------------------------

def test_create_money_with_decimal():
    money = Money(Decimal("10.50"))

    assert money.amount == Decimal("10.50")


def test_create_money_with_int():
    money = Money(10)

    assert money.amount == Decimal("10.00")


def test_create_money_with_string():
    money = Money("15.75")

    assert money.amount == Decimal("15.75")


def test_create_money_with_invalid_type():
    with pytest.raises(MoneyInvalidTypeError):
        Money(object())


# ----------------------------------------
# Teste de arredondamento (quantize)
# ----------------------------------------

def test_money_rounding():
    money = Money("10.555")

    assert money.amount == Decimal("10.56")


# ----------------------------------------
# Teste de valor negativo
# ----------------------------------------

def test_money_cannot_be_negative():
    with pytest.raises(MoneyInvalidValueError):
        Money("-10.00")


# ----------------------------------------
# Testes de operações add
# ----------------------------------------

def test_add_money():
    m1 = Money("10.00")
    m2 = Money("5.50")

    result = m1.add(m2)

    assert result.amount == Decimal("15.50")


def test_add_invalid_type():
    m1 = Money("10.00")

    with pytest.raises(MoneyInvalidTypeError):
        m1.add(10)


# ----------------------------------------
# Testes de operações subtract
# ----------------------------------------

def test_subtract_money():
    m1 = Money("10.00")
    m2 = Money("5.00")

    result = m1.subtract(m2)

    assert result.amount == Decimal("5.00")


def test_subtract_result_negative():
    m1 = Money("5.00")
    m2 = Money("10.00")

    with pytest.raises(MoneyInvalidValueError):
        m1.subtract(m2)


def test_subtract_invalid_type():
    m1 = Money("10.00")

    with pytest.raises(MoneyInvalidTypeError):
        m1.subtract(5)


# ----------------------------------------
# Testes de comparação
# ----------------------------------------

def test_money_equality():
    m1 = Money("10.00")
    m2 = Money("10.00")

    assert m1 == m2


def test_money_inequality():
    m1 = Money("10.00")
    m2 = Money("20.00")

    assert m1 != m2


def test_money_less_than():
    assert Money("5.00") < Money("10.00")


def test_money_less_or_equal():
    assert Money("10.00") <= Money("10.00")


def test_money_greater_than():
    assert Money("20.00") > Money("10.00")


def test_money_greater_or_equal():
    assert Money("10.00") >= Money("10.00")


# ----------------------------------------
# Teste de hash
# ----------------------------------------

def test_money_hash():
    m1 = Money("10.00")
    m2 = Money("10.00")

    assert hash(m1) == hash(m2)


# ----------------------------------------
# Teste de imutabilidade
# ----------------------------------------

def test_money_is_immutable():
    money = Money("10.00")

    with pytest.raises(MoneyError):
        money.amount = Decimal("20.00")


# ----------------------------------------
# Teste de __str__
# ----------------------------------------

def test_str_returns_formatted_value():
    money = Money("10.50")

    assert str(money) == "R$ 10.50"


# ----------------------------------------
# Teste de __repr__
# ----------------------------------------

def test_repr_contains_class_name():
    money = Money("10.50")

    representation = repr(money)

    assert "Money(" in representation
    assert "10.50" in representation


# ----------------------------------------
# Teste property-based com Hypothesis
# ----------------------------------------

@given(
    value=st.decimals(
        min_value=0,
        max_value=100000,
        allow_nan=False,
        allow_infinity=False,
    )
)
def test_money_never_breaks_with_random_values(value):

    money = Money(value)

    assert isinstance(money.amount, Decimal)
    assert money.amount >= Decimal("0")
    assert isinstance(str(money), str)
    assert isinstance(repr(money), str)