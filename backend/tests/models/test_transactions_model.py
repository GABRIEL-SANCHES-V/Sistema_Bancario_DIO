import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

import pytest
from datetime import datetime
from decimal import Decimal
from models import Transaction, TransactionType

@pytest.mark.parametrize(
    "transaction_type, value, date",
    [
        (TransactionType.DEPOSIT, Decimal("100.00"), datetime.strptime("01/01/2024", "%d/%m/%Y").date()),
        (TransactionType.WITHDRAW, Decimal("50.00"), datetime.strptime("02/01/2024", "%d/%m/%Y").date()),
        (TransactionType.DEPOSIT, Decimal("200.00"), datetime.strptime("03/01/2024", "%d/%m/%Y").date()),
    ],
)

def test_transaction_creation(transaction_type, value, date):
    """Testa a criação de uma transação com valores válidos."""
    transaction = Transaction(transaction_type, value, date)

    assert transaction.type_transaction == transaction_type
    assert transaction.value == value
    assert transaction.date == date

def test_invalid_transaction_type():
    """Testa a criação de uma transação com um tipo inválido, esperando que uma exceção seja levantada."""
    with pytest.raises(ValueError):
        Transaction(None, Decimal("100.00"), datetime.strptime("32/13/2000", "%d/%m/%Y").date())
