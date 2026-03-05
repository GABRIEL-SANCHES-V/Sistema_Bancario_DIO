import os
import sys
import pytest
from decimal import Decimal
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from models import Account, Client, TransactionType
from services import AccountService


@pytest.fixture
def client():
    return Client(
        "Gabriel Sanches",
        "123.456.789-00",
        datetime.strptime("01/01/1990", "%d/%m/%Y").date()
    )


@pytest.fixture
def account(client):
    return Account(
        cliente=client,
        account_number=123456,
        password="password123",
        balance=Decimal("1000.00")
    )


@pytest.fixture
def account_service(account):
    return AccountService(account)


def test_account_service_creation(account_service):
    """
    Testa a criação do serviço de conta.
    """
    assert isinstance(account_service, AccountService)
    assert account_service._account is not None


def test_account_service_deposit(account_service, account):
    """
    Testa o depósito na conta.
    """
    account_service._account = account
    account_service.deposit(Decimal("500.00"))
    assert account.balance == Decimal("1500.00")


def test_account_service_withdraw(account_service, account):
    """
    Testa o saque na conta.
    """
    account_service._account = account
    account_service.withdraw(Decimal("200.00"))
    assert account.balance == Decimal("800.00")


def test_account_service_extract(account_service, account):
    """
    Testa a obtenção do extrato da conta.
    """
    account_service._account = account
    account_service.deposit(Decimal("500.00"))
    account_service.withdraw(Decimal("200.00"))

    extract = account_service.get_extract()

    assert len(extract) == 2
    assert extract[0].type_transaction == TransactionType.DEPOSIT
    assert extract[1].type_transaction == TransactionType.WITHDRAW


def test_invalid_deposit(account_service, account):
    """
    Testa o depósito de um valor inválido (negativo ou zero).
    """
    account_service._account = account

    with pytest.raises(ValueError):
        account_service.deposit(Decimal("-100.00"))

    with pytest.raises(ValueError):
        account_service.deposit(Decimal("0.00"))


def test_invalid_withdraw(account_service, account):
    """
    Testa o saque de um valor inválido (negativo ou zero).
    """
    account_service._account = account

    with pytest.raises(ValueError):
        account_service.withdraw(Decimal("-100.00"))

    with pytest.raises(ValueError):
        account_service.withdraw(Decimal("0.00"))


def test_withdraw_exceeding_limit(account_service, account):
    """
    Testa o saque de um valor que excede o limite permitido.
    """
    account_service._account = account

    with pytest.raises(ValueError):
        account_service.withdraw(Decimal("600.00"))


def test_withdraw_exceeding_limit_daily(account_service, account):
    """
    Testa o saque que excede o limite diário de saques.
    """
    account_service._account = account

    account_service.withdraw(Decimal("100.00"))
    account_service.withdraw(Decimal("100.00"))
    account_service.withdraw(Decimal("100.00"))

    with pytest.raises(ValueError):
        account_service.withdraw(Decimal("100.00"))