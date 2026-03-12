from domains.value_objects.zip_code import ZipCode
from domains.value_objects.address import Address
from hypothesis import given, strategies as st
from domains.value_objects.state import State
from domains.exceptions import (
    AddressError,
    AddressInvalidTypeStateError,
    AddressInvalidTypeZipCodeError,
    AddressInvalidTypeError,
    AddressInvalidValueError,
)
import pytest


# ----------------------------------------
# Testes de criação e validação de Address
# ----------------------------------------

def test_create_valid_address():
    state = State("São Paulo")
    zip_code = ZipCode("12345-678")
    address = Address(
        "Rua A",
        "123",
        "Bairro B",
        "Cidade C",
        state,
        zip_code,
        "Brasil",
        "Complemento D",
    )

    assert address.street == "Rua A"
    assert address.number == "123"
    assert address.neighborhood == "Bairro B"
    assert address.city == "Cidade C"
    assert address.state == state
    assert address.zip_code == zip_code
    assert address.country == "Brasil"
    assert address.complement == "Complemento D"
    assert address.formatted == (
        "Rua A, 123 - Complemento D - Bairro B\n"
        "Cidade C - São Paulo (SP) - Brasil\n"
        "12345-678"
    )


def test_create_address_with_invalid_state_type():
    zip_code = ZipCode("12345-678")

    with pytest.raises(AddressInvalidTypeStateError):
        Address(
            "Rua A",
            "123",
            "Bairro B",
            "Cidade C",
            "São Paulo",
            zip_code,
            "Brasil",
        )


def test_create_address_with_invalid_zip_code_type():
    state = State("São Paulo")

    with pytest.raises(AddressInvalidTypeZipCodeError):
        Address(
            "Rua A",
            "123",
            "Bairro B",
            "Cidade C",
            state,
            "12345-678",
            "Brasil",
        )


def test_create_address_with_invalid_street_type():
    state = State("São Paulo")
    zip_code = ZipCode("12345-678")

    with pytest.raises(AddressInvalidTypeError):
        Address(
            123,
            "123",
            "Bairro B",
            "Cidade C",
            state,
            zip_code,
            "Brasil",
        )


# ----------------------------------------
# Testes de Validação de Address
# ----------------------------------------

@pytest.mark.parametrize(
    "street,number,neighborhood,city,state,zip_code,country,expected",
    [
        (
            "Rua A",
            "123",
            "Bairro B",
            "Cidade C",
            State("São Paulo"),
            ZipCode("12345-678"),
            "Brasil",
            True,
        ),
    ],
)
def test_is_valid_address(
    street: str,
    number: str,
    neighborhood: str,
    city: str,
    state: State,
    zip_code: ZipCode,
    country: str,
    expected: bool,
):
    assert (
        Address.is_valid(
            street,
            number,
            neighborhood,
            city,
            state,
            zip_code,
            country,
        )
        is expected
    )


@pytest.mark.parametrize(
    "street,number,neighborhood,city,state,zip_code,country,expected",
    [
        (
            123,
            "123",
            "Bairro B",
            "Cidade C",
            State("São Paulo"),
            ZipCode("12345-678"),
            "Brasil",
            False,
        ),
    ],
)
def test_is_invalid_address(
    street: str,
    number: str,
    neighborhood: str,
    city: str,
    state: State,
    zip_code: ZipCode,
    country: str,
    expected: bool,
):
    assert (
        Address.is_valid(
            street,
            number,
            neighborhood,
            city,
            state,
            zip_code,
            country,
        )
        is expected
    )


# ----------------------------------------
# Testes de campos obrigatórios
# ----------------------------------------

@pytest.mark.parametrize(
    "street,number,neighborhood,city,country",
    [
        ("", "123", "Bairro", "Cidade", "Brasil"),
        ("Rua", "", "Bairro", "Cidade", "Brasil"),
        ("Rua", "123", "", "Cidade", "Brasil"),
        ("Rua", "123", "Bairro", "", "Brasil"),
        ("Rua", "123", "Bairro", "Cidade", ""),
    ],
)
def test_required_fields_validation(
    street,
    number,
    neighborhood,
    city,
    country,
):
    state = State("São Paulo")
    zip_code = ZipCode("12345-678")

    with pytest.raises(AddressInvalidValueError):
        Address(
            street,
            number,
            neighborhood,
            city,
            state,
            zip_code,
            country,
        )


# ----------------------------------------
# Teste de normalização de strings
# ----------------------------------------

def test_string_normalization():
    state = State("São Paulo")
    zip_code = ZipCode("12345-678")

    address = Address(
        "  rua a  ",
        "123",
        " bairro b ",
        " cidade c ",
        state,
        zip_code,
        " brasil ",
    )

    assert address.street == "Rua A"
    assert address.neighborhood == "Bairro B"
    assert address.city == "Cidade C"
    assert address.country == "Brasil"


# ----------------------------------------
# Teste de número convertido para string
# ----------------------------------------

def test_number_converted_to_string():
    state = State("São Paulo")
    zip_code = ZipCode("12345-678")

    address = Address(
        "Rua A",
        123,
        "Bairro B",
        "Cidade C",
        state,
        zip_code,
    )

    assert address.number == "123"


# ----------------------------------------
# Teste sem complemento
# ----------------------------------------

def test_formatted_without_complement():
    state = State("São Paulo")
    zip_code = ZipCode("12345-678")

    address = Address(
        "Rua A",
        "123",
        "Bairro B",
        "Cidade C",
        state,
        zip_code,
    )

    assert address.formatted == (
        "Rua A, 123 - Bairro B\n"
        "Cidade C - São Paulo (SP) - Brasil\n"
        "12345-678"
    )


# ----------------------------------------
# Testes de igualdade
# ----------------------------------------

def test_address_equality():
    state = State("São Paulo")
    zip_code = ZipCode("12345-678")

    addr1 = Address(
        "Rua A",
        "123",
        "Bairro B",
        "Cidade C",
        state,
        zip_code,
    )

    addr2 = Address(
        "Rua A",
        "123",
        "Bairro B",
        "Cidade C",
        state,
        zip_code,
    )

    assert addr1 == addr2


def test_address_inequality():
    state = State("São Paulo")
    zip_code = ZipCode("12345-678")

    addr1 = Address(
        "Rua A",
        "123",
        "Bairro B",
        "Cidade C",
        state,
        zip_code,
    )

    addr2 = Address(
        "Rua B",
        "123",
        "Bairro B",
        "Cidade C",
        state,
        zip_code,
    )

    assert addr1 != addr2


# ----------------------------------------
# Teste de hash
# ----------------------------------------

def test_address_hash():
    state = State("São Paulo")
    zip_code = ZipCode("12345-678")

    addr1 = Address(
        "Rua A",
        "123",
        "Bairro B",
        "Cidade C",
        state,
        zip_code,
    )

    addr2 = Address(
        "Rua A",
        "123",
        "Bairro B",
        "Cidade C",
        state,
        zip_code,
    )

    assert hash(addr1) == hash(addr2)


# ----------------------------------------
# Teste de imutabilidade
# ----------------------------------------

def test_address_is_immutable():
    state = State("São Paulo")
    zip_code = ZipCode("12345-678")

    address = Address(
        "Rua A",
        "123",
        "Bairro B",
        "Cidade C",
        state,
        zip_code,
    )

    with pytest.raises(AddressError):
        address.street = "Rua B"


# ----------------------------------------
# Teste de __str__
# ----------------------------------------

def test_str_returns_formatted():
    state = State("São Paulo")
    zip_code = ZipCode("12345-678")

    address = Address(
        "Rua A",
        "123",
        "Bairro B",
        "Cidade C",
        state,
        zip_code,
    )

    assert str(address) == address.formatted


# ----------------------------------------
# Teste de __repr__
# ----------------------------------------

def test_repr_contains_class_name():
    state = State("São Paulo")
    zip_code = ZipCode("12345-678")

    address = Address(
        "Rua A",
        "123",
        "Bairro B",
        "Cidade C",
        state,
        zip_code,
    )

    representation = repr(address)

    assert "Address(" in representation
    assert "street='Rua A'" in representation


# ----------------------------------------
# Teste property-based com Hypothesis
# ----------------------------------------

@given(
    street=st.text(min_size=1),
    number=st.text(min_size=1),
    neighborhood=st.text(min_size=1),
    city=st.text(min_size=1),
)
def test_address_never_breaks_with_random_strings(
    street,
    number,
    neighborhood,
    city,
):
    state = State("São Paulo")
    zip_code = ZipCode("12345-678")

    address = Address(
        street,
        number,
        neighborhood,
        city,
        state,
        zip_code,
    )

    assert isinstance(address.street, str)
    assert isinstance(address.city, str)
    assert isinstance(address.neighborhood, str)
    assert isinstance(address.number, str)
    assert isinstance(address.country, str)
    assert isinstance(address.state, State)
    assert isinstance(address.zip_code, ZipCode)
    assert isinstance(address.formatted, str)