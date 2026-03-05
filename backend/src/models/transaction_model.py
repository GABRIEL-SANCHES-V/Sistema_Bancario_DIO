from datetime import datetime
from decimal import Decimal
from datetime import date
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
    def __init__(self, type_transaction: TransactionType, value: Decimal, date: date):
        self._type_transaction = type_transaction
        self._value = value
        self._date = date
    
    @property
    def type_transaction(self) -> TransactionType:
        return self._type_transaction

    @property
    def value(self) -> Decimal:
        return self._value
    
    @property
    def date(self) -> date:
        return self._date