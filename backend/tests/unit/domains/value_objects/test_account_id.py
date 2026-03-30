from hypothesis import given, strategies as st
from domains.value_objects.account_id import AccountID
from domains.exceptions import (
    AccountIdError,
    AccountIdInvalidTypeError,
)
import uuid
import pytest


UUID_1 = uuid.UUID("12345678-1234-5678-1234-567812345678")
UUID_1_STR = "12345678-1234-5678-1234-567812345678"

UUID_2 = uuid.UUID("87654321-4321-8765-4321-876543218765")
UUID_2_STR = "87654321-4321-8765-4321-876543218765"


# ----------------------------------------
# Testes de criação
# ----------------------------------------

def test_create_account_id_from_uuid():
    cid = AccountID(UUID_1)

    assert cid.value == UUID_1
    assert cid.hex == UUID_1.hex


def test_create_account_id_from_string():
    cid = AccountID(UUID_1_STR)

    assert cid.value == UUID_1
    assert cid.hex == UUID_1.hex


def test_create_account_id_auto_generation():
    cid = AccountID()

    assert isinstance(cid.value, uuid.UUID)
    assert isinstance(cid.hex, str)


# ----------------------------------------
# Testes de exceções
# ----------------------------------------

@pytest.mark.parametrize(
    "value",
    [
        123,
        3.14,
        [],
        {},
        object(),
    ],
)
def test_invalid_type_raises_exception(value):
    with pytest.raises(AccountIdInvalidTypeError):
        AccountID(value)


@pytest.mark.parametrize(
    "value",
    [
        "not-a-uuid",
        "1234",
        "invalid-uuid-format",
    ],
)
def test_invalid_uuid_string_raises_exception(value):
    with pytest.raises(ValueError):
        AccountID(value)


# ----------------------------------------
# Testes de propriedades
# ----------------------------------------

def test_account_id_properties():
    cid = AccountID(UUID_1)

    assert cid.value == UUID_1
    assert cid.hex == UUID_1.hex


# ----------------------------------------
# Testes de igualdade
# ----------------------------------------

def test_account_id_equality():
    cid1 = AccountID(UUID_1)
    cid2 = AccountID(UUID_1_STR)

    assert cid1 == cid2


def test_account_id_inequality():
    cid1 = AccountID(UUID_1)
    cid2 = AccountID(UUID_2)

    assert cid1 != cid2


def test_account_id_not_equal_other_type():
    cid = AccountID(UUID_1)

    assert cid != UUID_1


# ----------------------------------------
# Teste de hash
# ----------------------------------------

def test_account_id_hash():
    cid1 = AccountID(UUID_1)
    cid2 = AccountID(UUID_1_STR)

    assert hash(cid1) == hash(cid2)


def test_account_id_set_behavior():
    cid1 = AccountID(UUID_1)
    cid2 = AccountID(UUID_1_STR)

    s = {cid1, cid2}

    assert len(s) == 1


# ----------------------------------------
# Teste de imutabilidade
# ----------------------------------------

def test_account_id_is_immutable():
    cid = AccountID(UUID_1)

    with pytest.raises(AccountIdError):
        cid.value = UUID_2


# ----------------------------------------
# Teste de __str__
# ----------------------------------------

def test_str_returns_uuid_string():
    cid = AccountID(UUID_1)

    assert str(cid) == UUID_1_STR


# ----------------------------------------
# Teste de __repr__
# ----------------------------------------

def test_repr_contains_class_name():
    cid = AccountID(UUID_1)

    representation = repr(cid)

    assert "AccountID(" in representation
    assert UUID_1_STR in representation


# ----------------------------------------
# Property-based tests (Hypothesis)
# ----------------------------------------

@given(st.uuids())
def test_account_id_never_breaks_with_random_uuids(uuid_value):
    cid = AccountID(uuid_value)

    assert isinstance(cid.value, uuid.UUID)
    assert isinstance(cid.hex, str)


@given(st.uuids())
def test_account_id_equality_property(uuid_value):
    cid1 = AccountID(uuid_value)
    cid2 = AccountID(str(uuid_value))

    assert cid1 == cid2


@given(st.text())
def test_random_invalid_strings(value):
    try:
        uuid.UUID(value)
    except Exception:
        with pytest.raises(ValueError):
            AccountID(value)
