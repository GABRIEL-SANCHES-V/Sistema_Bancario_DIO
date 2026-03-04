from datetime import datetime
from decimal import Decimal
from enum import Enum

class TransactionType(Enum):
    DEPOSIT = "Depósito"
    WITHDRAW = "Saque"
    

class Transaction:
    """
        Represents a bank transaction.

        Attributes:
            type_transaction (TransactionType): Transaction type.
            value (Decimal): Transaction value.
            date (date): Transaction date.
    """
    def __init__(self, type_transaction: TransactionType, value: Decimal, date: str):
        self._type_transaction = type_transaction
        self._value = value
        self._date = datetime.strptime(date, "%d/%m/%Y").date()
    
    @property
    def type_transaction(self):
        return self._type_transaction

    @property
    def value(self):
        return self._value
    
    @property
    def date(self):
        return self._date