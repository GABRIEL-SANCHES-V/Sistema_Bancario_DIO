from decimal import Decimal
from .client_model import Client
from .transaction_model import Transaction
from typing import List


class Account():
    """
        Represents a bank account.

        Attributes:
            cliente (Client): The client who owns the account.
            account_number (int): The account number.
            withdraws_today (int): The number of withdrawals made today.
            balance (Decimal): The current balance of the account.
            extract (list): A list of transactions made on the account.
            password (str): The password for account access.
    """
    def __init__(self, cliente: Client, account_number: int,  password: str, balance: Decimal = Decimal("0.00")):
        self._cliente = cliente
        self._account_number = account_number
        self._withdraws_today = 0
        self._balance = balance
        self._extract = []
        self._password = password

    @property
    def cliente(self) -> Client:
        return self._cliente

    @property
    def account_number(self) -> int:
        return self._account_number
    
    @property
    def balance(self):
        return self._balance
    
    def increment_balance(self, value: Decimal):
        self._balance += value

    def decrement_balance(self, value: Decimal):
        self._balance -= value

    @property
    def withdraws_today(self) -> int:
        return self._withdraws_today
    
    def increment_withdraws_today(self):
        self._withdraws_today += 1

    def reset_withdraws_today(self):
        self._withdraws_today = 0

    @property
    def extract(self) -> List:
        return list(self._extract)
    
    def add_transaction_to_extract(self, transaction: Transaction):
        self._extract.append(transaction)
    
    @property
    def password(self) -> str:
        return self._password
    
    @password.setter
    def password(self, password: str):
        self._password = password
