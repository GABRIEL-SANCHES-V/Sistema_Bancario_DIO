from domains.entities.transactions import Transaction, TypeTransaction, StatusTransaction
from domains.value_objects import Money, AccountID, TransactionID
from domains.exceptions import (
    TransactionAttributeError,
    TransactionDepositError,
    TransactionWithdrawalError,
    TransactionTransferError,
    TransactionStatusTransitionError,
)

import pytest


@pytest.fixture
def valid_deposit():
    return Transaction(
        amount=Money(100),
        type_transaction=TypeTransaction.DEPOSIT,
        to_account=AccountID(),
    )


@pytest.fixture
def valid_transfer():
    return Transaction(
        amount=Money(200),
        type_transaction=TypeTransaction.TRANSFER,
        from_account=AccountID(),
        to_account=AccountID(),
    )


# ---------------------------------------------------------------
# Testes de Criação
# ---------------------------------------------------------------

def test_transaction_creation(valid_deposit):
    assert valid_deposit.amount == Money(100)
    assert valid_deposit.type_transaction == TypeTransaction.DEPOSIT
    assert valid_deposit.status == StatusTransaction.PENDING
    assert valid_deposit.timestamp is not None


# ---------------------------------------------------------------
# Testes de Regras de Domínio
# ---------------------------------------------------------------

def test_deposit_without_destination_account():
    with pytest.raises(TransactionDepositError):
        Transaction(
            amount=Money(100),
            type_transaction=TypeTransaction.DEPOSIT,
        )


def test_withdrawal_without_origin_account():
    with pytest.raises(TransactionWithdrawalError):
        Transaction(
            amount=Money(100),
            type_transaction=TypeTransaction.WITHDRAWAL,
        )


def test_transfer_without_accounts():
    with pytest.raises(TransactionTransferError):
        Transaction(
            amount=Money(100),
            type_transaction=TypeTransaction.TRANSFER,
            from_account=AccountID(),
        )


# ---------------------------------------------------------------
# Testes de Transição de Estado
# ---------------------------------------------------------------

def test_mark_transaction_as_successful(valid_deposit):
    valid_deposit.mark_as_successful()
    assert valid_deposit.status == StatusTransaction.SUCCESSFUL


def test_mark_transaction_as_failed(valid_deposit):
    valid_deposit.mark_as_failed()
    assert valid_deposit.status == StatusTransaction.FAILED


def test_invalid_status_transition(valid_deposit):
    valid_deposit.mark_as_successful()

    with pytest.raises(TransactionStatusTransitionError):
        valid_deposit.mark_as_failed()


# ---------------------------------------------------------------
# Testes de Imutabilidade
# ---------------------------------------------------------------

def test_transaction_immutability(valid_deposit):

    with pytest.raises(TransactionAttributeError):
        valid_deposit.amount = Money(999)

    with pytest.raises(TransactionAttributeError):
        valid_deposit.timestamp = None