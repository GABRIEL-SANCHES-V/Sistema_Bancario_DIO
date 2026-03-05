import os
import sys
import pytest
from decimal import Decimal
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from models import Account, Client, Transaction, TransactionType


@pytest.fixture
def client():
    return Client("Gabriel Sanches", "123.456.789-00", datetime.strptime("01/01/1990", "%d/%m/%Y").date())


@pytest.fixture
def account(client):
    return Account(
        cliente=client,
        account_number=123456,
        password="password123",
        balance=Decimal("1000.00")
    )


def test_account_creation(account, client):
    """Testa a criação de uma conta com valores válidos."""
    assert account.cliente == client
    assert account.account_number == 123456
    assert account.balance == Decimal("1000.00")
    assert account.withdraws_today == 0
    assert account.extract == []
    assert account.password == "password123"



def test_increment_balance(account):
    """Testa o incremento do saldo da conta."""
    account.increment_balance(Decimal("500.00"))
    assert account.balance == Decimal("1500.00")


def test_decrement_balance(account):
    """Testa o decremento do saldo da conta."""
    account.decrement_balance(Decimal("200.00"))
    assert account.balance == Decimal("800.00")


def test_decrement_balance_full(account):
    """Testa o decremento do saldo da conta até zero."""
    account.decrement_balance(Decimal("1000.00"))
    assert account.balance == Decimal("0.00")


def test_withdraws_today(account):
    """Testa o incremento do número de saques realizados hoje."""
    account.increment_withdraws_today()
    account.increment_withdraws_today()
    assert account.withdraws_today == 2

    account.reset_withdraws_today()
    assert account.withdraws_today == 0


def test_add_transaction_to_extract(account):
    """Testa a adição de uma transação à extrato da conta."""
    transaction = Transaction(
        TransactionType.DEPOSIT,
        Decimal("100.00"),
        datetime.strptime("01/01/2024", "%d/%m/%Y").date()
    )

    account.add_transaction_to_extract(transaction)

    assert len(account.extract) == 1
    assert account.extract[0] == transaction


def test_extract_immutability(account):
    """Testa a imutabilidade do extrato da conta."""
    transaction = Transaction(
        TransactionType.DEPOSIT,
        Decimal("100.00"),
        datetime.strptime("01/01/2024", "%d/%m/%Y").date()
    )

    account.add_transaction_to_extract(transaction)

    external_extract = account.extract
    external_extract.append("fake")

    assert len(account.extract) == 1


def test_password_setter(account):
    """Testa a funcionalidade do setter de senha da conta."""
    account.password = "new_password"
    assert account.password == "new_password"


def test_invalid_account_creation_missing_account_number(client):
    """Testa a criação de uma conta sem o número da conta, esperando que uma exceção seja levantada."""
    with pytest.raises(TypeError):
        Account(cliente=client, password="123", balance=Decimal("1000.00"))


def test_invalid_account_creation_missing_password(client):
    """Testa a criação de uma conta sem a senha, esperando que uma exceção seja levantada."""
    with pytest.raises(TypeError):
        Account(cliente=client, account_number=123456, balance=Decimal("1000.00"))