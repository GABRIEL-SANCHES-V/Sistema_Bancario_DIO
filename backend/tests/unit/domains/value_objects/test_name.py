from domains.value_objects.name import Name, MIN_NAME_LENGTH, MAX_NAME_LENGTH
from domains.exceptions import (
    NameInvalidTypeError,
    NameTooShortError,
    NameTooLongError,
    NameInvalidFormatError,
    NameErrorVO,
)
from hypothesis import given, strategies as st
import pytest


# ----------------------------------------
# Testes de criação e validação de Name
# ----------------------------------------

def test_create_valid_name():
    name = Name("Joao Silva")

    assert name.name == "Joao Silva"


def test_create_name_with_invalid_type():
    with pytest.raises(NameInvalidTypeError):
        Name(123)


# ----------------------------------------
# Testes de tamanho mínimo
# ----------------------------------------

def test_name_too_short():
    short_name = "Ana"

    with pytest.raises(NameTooShortError):
        Name(short_name)


# ----------------------------------------
# Testes de tamanho máximo
# ----------------------------------------

def test_name_too_long():
    long_name = "A" * (MAX_NAME_LENGTH + 1)

    with pytest.raises(NameTooLongError):
        Name(long_name)


# ----------------------------------------
# Testes de formato inválido
# ----------------------------------------

@pytest.mark.parametrize(
    "invalid_name",
    [
        "Joao123",
        "Joao_Silva",
        "Joao-Silva",
        "Joao@Silva",
        "12345678",
    ],
)
def test_invalid_name_format(invalid_name):
    with pytest.raises(NameErrorVO):
        Name(invalid_name)


# ----------------------------------------
# Teste de normalização de string
# ----------------------------------------

def test_name_normalization():
    name = Name("   joao silva   ")

    assert name.name == "Joao Silva"


# ----------------------------------------
# Testes de Validação com is_valid
# ----------------------------------------

@pytest.mark.parametrize(
    "value,expected",
    [
        ("Joao Silva", True),
        ("Ana", False),
        ("Joao123", False),
        (123, False),
    ],
)
def test_is_valid(value, expected):
    assert Name.is_valid(value) is expected


# ----------------------------------------
# Testes de igualdade
# ----------------------------------------

def test_name_equality():
    name1 = Name("Joao Silva")
    name2 = Name("Joao Silva")

    assert name1 == name2


def test_name_inequality():
    name1 = Name("Joao Silva")
    name2 = Name("Maria Silva")

    assert name1 != name2


# ----------------------------------------
# Teste de hash
# ----------------------------------------

def test_name_hash():
    name1 = Name("Joao Silva")
    name2 = Name("Joao Silva")

    assert hash(name1) == hash(name2)


# ----------------------------------------
# Teste de imutabilidade
# ----------------------------------------

def test_name_is_immutable():
    name = Name("Joao Silva")

    with pytest.raises(NameErrorVO):
        name.name = "Maria Silva"


# ----------------------------------------
# Teste de __str__
# ----------------------------------------

def test_str_returns_name():
    name = Name("Joao Silva")

    assert str(name) == "Joao Silva"


# ----------------------------------------
# Teste de __repr__
# ----------------------------------------

def test_repr_contains_class_name():
    name = Name("Joao Silva")

    representation = repr(name)

    assert "Name(" in representation
    assert "Joao Silva" in representation


# ----------------------------------------
# Teste property-based com Hypothesis
# ----------------------------------------

@given(
    st.text(
        alphabet=st.characters(
            whitelist_categories=("Ll", "Lu"),
            whitelist_characters=" "
        ),
        min_size=MIN_NAME_LENGTH,
        max_size=MAX_NAME_LENGTH,
    )
)
def test_name_never_breaks_with_random_valid_strings(value):
    if Name.is_valid(value):
        name = Name(value)

        assert isinstance(name.name, str)
        assert isinstance(str(name), str)
        assert isinstance(repr(name), str)