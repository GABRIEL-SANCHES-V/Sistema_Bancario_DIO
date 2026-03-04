import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from datetime import date
from models import Client


@pytest.fixture
def client():
    return Client("Gabriel Sanches", "123.456.789-00", "01/01/1990")


def test_client_creation(client):
    """
        Testa a criação de um cliente com valores válidos.
    """
    assert client.name == "Gabriel Sanches"
    assert client.cpf == "123.456.789-00"
    assert client.date_of_birth == date(1990, 1, 1)


def test_age_calculation(client):
    """
        Testa o cálculo da idade do cliente.
    """
    today = date.today()
    birth = client.date_of_birth

    expected_age = today.year - birth.year - (
        (today.month, today.day) < (birth.month, birth.day)
    )

    assert client.age == expected_age

def test_invalid_date():
    """
        Testa a criação de um cliente com uma data inválida, esperando que uma exceção seja levantada.
    """
    with pytest.raises(ValueError):
        Client("Gabriel", "123", "32/13/2000")