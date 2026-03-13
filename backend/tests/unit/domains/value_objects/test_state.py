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


# ----------------------------------------
# Testes de criação e validação
# ----------------------------------------

@pytest.mark.parametrize(
    "state_name,uf",
    list(DICT_STATES.items()),
)
def test_create_valid_state_from_name(state_name, uf):
    state = State(state_name)

    assert state.state == state_name
    assert state.uf == uf
    assert state.formatted == f"{state_name} ({uf})"


@pytest.mark.parametrize(
    "state_name,uf",
    list(DICT_STATES.items()),
)
def test_create_valid_state_from_uf(state_name, uf):
    state = State(uf)

    assert state.state == state_name
    assert state.uf == uf
    assert state.formatted == f"{state_name} ({uf})"


def test_create_state_with_invalid_type():
    with pytest.raises(StateInvalidTypeError):
        State(123)


# ----------------------------------------
# Testes de normalização
# ----------------------------------------

def test_state_string_normalization():
    state = State("  são paulo  ")

    assert state.state == "São Paulo"
    assert state.uf == "SP"


def test_state_accepts_lowercase_uf():
    state = State("sp")

    assert state.state == "São Paulo"
    assert state.uf == "SP"


# ----------------------------------------
# Testes de validação pública
# ----------------------------------------

@pytest.mark.parametrize(
    "value",
    list(DICT_STATES.keys()),
)
def test_is_valid_from_state_name(value):
    assert State.is_valid(value) is True


@pytest.mark.parametrize(
    "value",
    list(DICT_STATES.values()),
)
def test_is_valid_from_uf(value):
    assert State.is_valid(value) is True


@pytest.mark.parametrize(
    "value",
    [
        "Sao Paulo",
        "SSP",
        "Rio da Janeiro",
        "RJS",
        "InvalidState",
        "XX",
    ],
)
def test_is_invalid_state(value):
    assert State.is_valid(value) is False


@pytest.mark.parametrize(
    "value",
    [
        "Sao Paulo",
        "SSP",
        "Rio da Janeiro",
        "RJS",
        "InvalidState",
        "XX",
    ],
)
def test_invalid_state_raises_exception(value):
    with pytest.raises(StateInvalidError):
        State(value)


# ----------------------------------------
# Testes de igualdade
# ----------------------------------------

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


# ----------------------------------------
# Testes de hash
# ----------------------------------------

def test_state_hash():
    state1 = State("São Paulo")
    state2 = State("SP")
    state3 = State("Rio de Janeiro")

    assert hash(state1) == hash(state2)
    assert hash(state1) != hash(state3)


def test_state_as_dict_key():
    states = {
        State("SP"): "São Paulo",
        State("RJ"): "Rio de Janeiro",
    }

    assert states[State("São Paulo")] == "São Paulo"


# ----------------------------------------
# Testes de representação
# ----------------------------------------

def test_str_returns_formatted():
    state = State("São Paulo")

    assert str(state) == "São Paulo (SP)"


def test_repr_contains_class_name():
    state = State("São Paulo")

    representation = repr(state)

    assert "State(" in representation
    assert "'SP'" in representation


# ----------------------------------------
# Teste de imutabilidade
# ----------------------------------------

def test_state_is_immutable():
    state = State("São Paulo")

    with pytest.raises(StateError):
        state.state = "Rio de Janeiro"

    with pytest.raises(StateError):
        state.uf = "RJ"

    with pytest.raises(StateError):
        state.formatted = "Rio de Janeiro (RJ)"