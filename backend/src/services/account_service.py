import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from models import Account
from models import Transaction, TransactionType
from decimal import Decimal
import logging
from typing import List

logger = logging.getLogger(__name__)


class AccountService:
    """
        Represent a service for handling account operations such as deposits, withdrawals, and transaction history.

        Attributes:
            account (Account): The account associated with this service.
        
        Methods:
            deposit(value: float) -> dict: Deposits a specified amount into the account and returns a status message.
            withdraw(value: float) -> dict: Withdraws a specified amount from the account and returns a status message.
            get_extract() -> str: Retrieves the formatted transaction history (extract) of the account.
    """
    def __init__(self, account: Account):
        self._account = account


    def _add_transaction_to_extract(self, transaction: Transaction) -> None:
        """
            Adds a transaction to the account's extract.

            Args:
                transaction (Transaction): The transaction to be added to the extract.
            
            Returns:
                None
        """
        self._account.extract.append(transaction)
    

    def deposit(self, value: Decimal) -> None:
        """
            Deposits a specified amount into the account.

            Args:
                value (Decimal): The amount to be deposited. Must be a positive number.
            
            Returns:
                None
        """
        if value <= Decimal("0.00"):
            raise ValueError("Valor de depósito deve ser positivo!")
        
        try:
            self._account.increment_balance(value)

            self._add_transaction_to_extract(
                Transaction(TransactionType.DEPOSIT, value, datetime.now())
            )

            logger.info(f"Depósito de R${value} realizado com sucesso!")

        except Exception as error:
            logger.exception(f"Erro ao depositar valor: {error}")
            raise


    def withdraw(self, value: Decimal) -> None:
        """
            Withdraws a specified amount from the account.

            Args:
                value (Decimal): The amount to be withdrawn. Must be a positive number.
            
            Returns:
                None
        """
        if value <= Decimal("0.00"):
            raise ValueError("Valor de saque deve ser positivo!")
        
        if value > self._account.balance:
            raise ValueError("Saldo insuficiente!")
        
        if self._account.withdraws_today >= 3:
            raise ValueError("Limite de saques diários atingido!")
        
        if value > Decimal("500.00"):
            raise ValueError("Valor de saque excede o limite permitido!")

        try:
            self._account.decrement_balance(value)

            self._add_transaction_to_extract(
                Transaction(TransactionType.WITHDRAW, value, datetime.now())
            )

            self._account.increment_withdraws_today()

            logger.info(f"Saque de R${value} realizado com sucesso!")

        except Exception as error:
            logger.exception(f"Erro ao sacar valor: {error}")
            raise
    
    
    def get_extract(self) -> List:
        """
            Retrieves the formatted transaction history (extract) of the account.

            Returns:
                List[Transaction]: A list of transactions representing the transaction history, or an empty list if no transactions have been made.
        """
        if not self._account.extract:
            return []
        
        return list(self._account.extract)