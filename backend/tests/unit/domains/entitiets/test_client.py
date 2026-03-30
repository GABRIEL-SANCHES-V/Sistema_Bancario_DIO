from domains.exceptions import ClientAttributeError
from domains.entities.client import Client
from domains.value_objects import (
    State,
    ZipCode,
    Address,
    Name,
    Email,
    PhoneNumber,
    BirthDate,
    CPF,
)
import pytest


@pytest.fixture
def valid_client():
    return Client(
        name=Name("John Doe"),
        email=Email("john.doe@example.com"),
        cpf=CPF("12345678909"),
        phone_number=PhoneNumber("11987654321"),
        birth_date=BirthDate("1990-01-01"),
        address=Address(
            street="Main Street",
            number="123",
            complement="Apt 4",
            neighborhood="Downtown",
            city="São Paulo",
            state=State("SP"),
            zip_code=ZipCode("12345-678")
        )
    )


# ---------------------------------------------------------------
# Testes de Criação de Cliente
# ---------------------------------------------------------------

def test_client_creation(valid_client):
    assert valid_client.name.name == "John Doe"
    assert valid_client.email.value == "john.doe@example.com"
    assert valid_client.cpf.value == "12345678909"
    assert valid_client.phone_number.formatted == "(11) 98765-4321"
    assert valid_client.birth_date.formatted_br == "01/01/1990"
    assert valid_client.address.street == "Main Street"
    assert valid_client.address.number == "123"
    assert valid_client.address.complement == "Apt 4"
    assert valid_client.address.neighborhood == "Downtown"
    assert valid_client.address.city == "São Paulo"
    assert valid_client.address.state.formatted == "São Paulo (SP)"
    assert valid_client.address.zip_code.formatted == "12345-678"
    assert valid_client.age == 36


# ---------------------------------------------------------------
# Testes de Imutabilidade
# ---------------------------------------------------------------

def test_client_immutability(valid_client):
    with pytest.raises(ClientAttributeError):
        valid_client.cpf = CPF("12345678909")


# ---------------------------------------------------------------
# Testes de Mutabilidade
# ---------------------------------------------------------------

def test_client_mutability(valid_client):
    new_name = Name("Jane Doe")
    valid_client.change_name(new_name)
    assert valid_client.name == new_name

    new_email = Email("jane.doe@example.com")
    valid_client.change_email(new_email)
    assert valid_client.email == new_email

    new_phone_number = PhoneNumber("11912345678")
    valid_client.change_phone_number(new_phone_number)
    assert valid_client.phone_number == new_phone_number
    
    new_address = Address(
        street="Second Street",
        number="456",
        complement="Apt 8",
        neighborhood="Uptown",
        city="Rio de Janeiro",
        state=State("RJ"),
        zip_code=ZipCode("87654-321")
    )
    valid_client.change_address(new_address)
    assert valid_client.address == new_address

    new_birth_date = BirthDate("1985-05-15")
    valid_client.change_birth_date(new_birth_date)
    assert valid_client.birth_date == new_birth_date
    assert valid_client.age == 40