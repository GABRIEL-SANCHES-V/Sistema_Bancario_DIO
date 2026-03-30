from hypothesis import given, strategies as st
from domains.value_objects.transaction_id import TransactionID
from domains.exceptions import (
    TransactionIdError,
    TransactionIdInvalidTypeError,
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

def test_create_transaction_id_from_uuid():
    tid = TransactionID(UUID_1)

    assert tid.value == UUID_1
    assert tid.hex == UUID_1.hex


def test_create_transaction_id_from_string():
    tid = TransactionID(UUID_1_STR)

    assert tid.value == UUID_1
    assert tid.hex == UUID_1.hex


def test_create_transaction_id_auto_generation():
    tid = TransactionID()

    assert isinstance(tid.value, uuid.UUID)
    assert isinstance(tid.hex, str)


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
    with pytest.raises(TransactionIdInvalidTypeError):
        TransactionID(value)


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
        TransactionID(value)


# ----------------------------------------
# Testes de propriedades
# ----------------------------------------

def test_transaction_id_properties():
    tid = TransactionID(UUID_1)

    assert tid.value == UUID_1
    assert tid.hex == UUID_1.hex


# ----------------------------------------
# Testes de igualdade
# ----------------------------------------

def test_transaction_id_equality():
    tid1 = TransactionID(UUID_1)
    tid2 = TransactionID(UUID_1_STR)

    assert tid1 == tid2


def test_transaction_id_inequality():
    tid1 = TransactionID(UUID_1)
    tid2 = TransactionID(UUID_2)

    assert tid1 != tid2


def test_transaction_id_not_equal_other_type():
    tid = TransactionID(UUID_1)

    assert tid != UUID_1


# ----------------------------------------
# Teste de hash
# ----------------------------------------

def test_transaction_id_hash():
    tid1 = TransactionID(UUID_1)
    tid2 = TransactionID(UUID_1_STR)

    assert hash(tid1) == hash(tid2)


def test_transaction_id_set_behavior():
    tid1 = TransactionID(UUID_1)
    tid2 = TransactionID(UUID_1_STR)

    s = {tid1, tid2}

    assert len(s) == 1


# ----------------------------------------
# Teste de imutabilidade
# ----------------------------------------

def test_transaction_id_is_immutable():
    tid = TransactionID(UUID_1)

    with pytest.raises(TransactionIdError):
        tid.value = UUID_2


# ----------------------------------------
# Teste de __str__
# ----------------------------------------

def test_str_returns_uuid_string():
    tid = TransactionID(UUID_1)

    assert str(tid) == UUID_1_STR


# ----------------------------------------
# Teste de __repr__
# ----------------------------------------

def test_repr_contains_class_name():
    tid = TransactionID(UUID_1)

    representation = repr(tid)

    assert "TransactionID(" in representation
    assert UUID_1_STR in representation


# ----------------------------------------
# Property-based tests (Hypothesis)
# ----------------------------------------

@given(st.uuids())
def test_transaction_id_never_breaks_with_random_uuids(uuid_value):
    tid = TransactionID(uuid_value)

    assert isinstance(tid.value, uuid.UUID)
    assert isinstance(tid.hex, str)


@given(st.uuids())
def test_transaction_id_equality_property(uuid_value):
    tid1 = TransactionID(uuid_value)
    tid2 = TransactionID(str(uuid_value))

    assert tid1 == tid2


@given(st.text())
def test_random_invalid_strings(value):
    try:
        uuid.UUID(value)
    except Exception:
        with pytest.raises(ValueError):
            TransactionID(value)
