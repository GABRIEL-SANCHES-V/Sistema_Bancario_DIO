from datetime import datetime, UTC
from typing import Optional
from enum import Enum

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
    """
        Entidade que representa uma transação bancária.

        Atributos:
            - transaction_id: Identificador único da transação (imutável)
            - amount: Valor da transação
            - type_transaction: Tipo da transação (deposito, saque, transferência, etc.)
            - from_account: Identificador da conta de origem (opcional)
            - to_account: Identificador da conta de destino (opcional)
            - status: Status da transação (pendente, bem-sucedida, falha)
            - timestamp: Data e hora da transação

        Métodos:
            - mark_as_successful: Marca a transação como bem-sucedida
            - mark_as_failed: Marca a transação como falha
            - is_credit_for: Verifica se a transação é um crédito para uma conta
            - is_debit_for: Verifica se a transação é um débito para uma conta
            - is_successful: Verifica se a transação é bem-sucedida
            - is_pending: Verifica se a transação está pendente
            - is_failed: Verifica se a transação falhou
    """

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
        self._timestamp = datetime.now(UTC)

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
    # Métodos de Negócio
    # ---------------------------------------------------------------

    def is_credit_for(self, account_id: AccountID) -> bool:
        return self._to_account == account_id

    def is_debit_for(self, account_id: AccountID) -> bool:
        return self._from_account == account_id

    def is_successful(self) -> bool:
        return self._status == StatusTransaction.SUCCESSFUL

    def is_pending(self) -> bool:
        return self._status == StatusTransaction.PENDING

    def is_failed(self) -> bool:
        return self._status == StatusTransaction.FAILED
    

    # ---------------------------------------------------------------
    # Representação
    # ---------------------------------------------------------------

    def __str__(self):
        return (
            f"{self._type_transaction.value.upper()} | "
            f"id={self._transaction_id} | "
            f"amount={self._amount} | "
            f"from={self._from_account} | "
            f"to={self._to_account} | "
            f"status={self._status.value} | "
            f"at={self._timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
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