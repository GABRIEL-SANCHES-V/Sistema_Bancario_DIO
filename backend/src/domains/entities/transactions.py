from enum import Enum
from datetime import datetime
from typing import Optional

from domains.value_objects import (
    Money,
    AccountID,
    TransactionID,
)

from domains.exceptions import (
    TransactionAttributeError,
    TransactionDepositError,
    TransactionWithdrawalError,
    TransactionTransferError,
    TransactionStatusTransitionError,
)


class TypeTransaction(Enum):
    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'
    TRANSFER = 'transfer'
    PAYMENT = 'payment'
    LOAN = 'loan'


class StatusTransaction(Enum):
    PENDING = 'pending'
    SUCCESSFUL = 'successful'
    FAILED = 'failed'


class Transaction:

    __slots__ = (
        '_transaction_id',
        '_from_account',
        '_to_account',
        '_amount',
        '_type_transaction',
        '_status',
        '_timestamp'
    )

    def __init__(
        self,
        amount: Money,
        type_transaction: TypeTransaction,
        from_account: Optional[AccountID] = None,
        to_account: Optional[AccountID] = None,
    ):
        self._transaction_id = TransactionID()
        self._amount = amount
        self._type_transaction = type_transaction
        self._from_account = from_account
        self._to_account = to_account
        self._status = StatusTransaction.PENDING
        self._timestamp = datetime.now()

        self._validate()

    # ---------------------------------------------------------------
    # Propriedades Imutáveis
    # ---------------------------------------------------------------

    @property
    def transaction_id(self):
        return self._transaction_id

    @property
    def type_transaction(self):
        return self._type_transaction

    @property
    def amount(self):
        return self._amount

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def from_account(self):
        return self._from_account

    @property
    def to_account(self):
        return self._to_account

    # ---------------------------------------------------------------
    # Propriedades Controladas
    # ---------------------------------------------------------------

    @property
    def status(self):
        return self._status

    # ---------------------------------------------------------------
    # Regras de Domínio
    # ---------------------------------------------------------------

    def _validate(self):

        if self._type_transaction == TypeTransaction.DEPOSIT:
            if not self._to_account:
                raise TransactionDepositError()

        elif self._type_transaction == TypeTransaction.WITHDRAWAL:
            if not self._from_account:
                raise TransactionWithdrawalError()

        elif self._type_transaction == TypeTransaction.TRANSFER:
            if not self._from_account or not self._to_account:
                raise TransactionTransferError()

    # ---------------------------------------------------------------
    # Transição de Estado
    # ---------------------------------------------------------------

    def mark_as_successful(self):
        if self._status != StatusTransaction.PENDING:
            raise TransactionStatusTransitionError(self._status.value, StatusTransaction.SUCCESSFUL.value)

        self._status = StatusTransaction.SUCCESSFUL

    def mark_as_failed(self):
        if self._status != StatusTransaction.PENDING:
            raise TransactionStatusTransitionError(self._status.value, StatusTransaction.FAILED.value)

        self._status = StatusTransaction.FAILED

    # ---------------------------------------------------------------
    # Representação
    # ---------------------------------------------------------------

    def __str__(self):
        return (
            f"\n{'-'*50}\n"
            f"Transaction ID: {self.transaction_id}\n"
            f"Type: {self.type_transaction.value}\n"
            f"Amount: {self.amount}\n"
            f"From: {self.from_account}\n"
            f"To: {self.to_account}\n"
            f"Status: {self.status.value}\n"
            f"Timestamp: {self.timestamp}\n"
            f"{'-'*50}"
        )

    def __repr__(self):
        return (
            f"Transaction(transaction_id={self.transaction_id}, "
            f"type_transaction={self.type_transaction}, "
            f"amount={self.amount}, "
            f"from_account={self.from_account}, "
            f"to_account={self.to_account}, "
            f"status={self.status}, "
            f"timestamp={self.timestamp})"
        )

    # ---------------------------------------------------------------
    # Imutabilidade Parcial
    # ---------------------------------------------------------------

    def __setattr__(self, key, value):
        if key in {
            "_transaction_id",
            "transaction_id",
            "_timestamp",
            "timestamp",
            "_type_transaction",
            "type_transaction",
            "_amount",
            "amount",
            "_to_account",
            "to_account",
            "_from_account",
            "from_account",
        } and hasattr(self, key):
            raise TransactionAttributeError(key)

        object.__setattr__(self, key, value)