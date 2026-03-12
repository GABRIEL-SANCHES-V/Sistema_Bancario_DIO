from domains.value_objects.state import (
    State,
    DICT_STATES,
)
from domains.exceptions import (
    StateError,
    StateInvalidTypeError,
    StateInvalidError,
)
import pytest


# -------------------------------------
# Creation tests
# -------------------------------------

def test_create_valid_state_from_state_name():
    for state_name, uf in DICT_STATES.items():
        state = State(state_name)
        assert state.state == state_name
        assert state.uf == uf
        assert state.formatted == f"{state_name} ({uf})"

def test_create_valid_state_from_uf():
    for state_name, uf in DICT_STATES.items():
        state = State(uf)
        assert state.state == state_name
        assert state.uf == uf
        assert state.formatted == f"{state_name} ({uf})"

def test_create_state_with_invalid_type():
    with pytest.raises(StateInvalidTypeError):
        State(123)


# -------------------------------------
# Normalization tests
# -------------------------------------

def test_state_normalization():
    state = State("  são paulo  ")

    assert state.state == "São Paulo"
    assert state.uf == "SP"


def test_state_accepts_lowercase_uf():
    state = State("sp")

    assert state.state == "São Paulo"
    assert state.uf == "SP"


# -------------------------------------
# Validation tests
# -------------------------------------

@pytest.mark.parametrize(
    "value,expected",
    [(state_name, True) for state_name in DICT_STATES]
)
def test_state_is_valid_from_state_name(value, expected):
    assert State.is_valid(value) is expected

@pytest.mark.parametrize(
    "value,expected",
    [(uf, True) for _, uf in DICT_STATES.items()]
)
def test_state_is_valid_from_uf(value, expected):
    assert State.is_valid(value) is expected

@pytest.mark.parametrize(
    "value,expected",
    [
        ("Sao Paulo", False),
        ("SSP", False),
        ("Rio da Janeiro", False),
        ("RJS", False),
        ("InvalidState", False),
        ("XX", False),
    ],
)
def test_state_is_valid(value, expected):
    assert State.is_valid(value) is expected

@pytest.mark.parametrize(
    "value,exception",
    [
        ("Sao Paulo", StateInvalidError),
        ("SSP", StateInvalidError),
        ("Rio da Janeiro", StateInvalidError),
        ("RJS", StateInvalidError),
        ("InvalidState", StateInvalidError),
        ("XX", StateInvalidError),
    ],
)
def test_invalid_state_raises_exception(value, exception):
    with pytest.raises(exception):
        State(value)


# -------------------------------------
# Igualdade tests
# -------------------------------------

def test_state_equality():
    state1 = State("São Paulo")
    state2 = State("SP")
    state3 = State("Rio de Janeiro")

    assert state1 == state2
    assert state1 != state3

def test_state_set_behavior():

    states = {
        State("SP"),
        State("São Paulo"),
        State("Rio de Janeiro"),
    }

    assert len(states) == 2


# -------------------------------------
# Hash tests
# -------------------------------------

def test_state_hash():
    state1 = State("São Paulo")
    state2 = State("SP")
    state3 = State("Rio de Janeiro")

    assert hash(state1) == hash(state2)
    assert hash(state1) != hash(state3)

def test_state_as_dict_key():

    d = {
        State("SP"): "São Paulo",
        State("RJ"): "Rio de Janeiro",
    }

    assert d[State("São Paulo")] == "São Paulo"


# -------------------------------------
# Representation tests
# -------------------------------------

def test_state_representation():
    state = State("São Paulo")
    repr_str = repr(state)

    assert repr_str == "State('SP')"
    assert str(state) == "São Paulo (SP)"
    assert state.formatted == "São Paulo (SP)"


# -------------------------------------
# Immutability tests
# -------------------------------------

def test_state_is_immutable():
    state = State("São Paulo")

    with pytest.raises(StateError):
        state.state = "Rio de Janeiro"

    with pytest.raises(StateError):
        state.uf = "RJ"

    with pytest.raises(StateError):
        state.formatted = "Rio de Janeiro (RJ)"

