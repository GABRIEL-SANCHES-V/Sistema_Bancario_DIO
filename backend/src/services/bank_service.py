import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .account_service import AccountService
from datetime import datetime
from decimal import Decimal
from models import Account
from models import Client
import logging

logger = logging.getLogger(__name__)


class ServiceBank:
    def __init__(self):
        self._clients = {}
        self._accounts = {}

    def _research_client(self, cpf: str):
        result = self._clients.get(cpf)

        if not result:
            return False
        
        return True

    def _research_account(self, account_number: int):
        result = self._accounts.get(account_number)

        if not result:
            return False
        
        return True

    def _creat_user(self, name: str, cpf: str, date_of_birth: str):

        if self._research_client(cpf):
            return {"Status": False, "Message": "Cliente Já cadastrado"}

        new_client = Client(name, cpf, date_of_birth)

        self._clients[cpf] = new_client

        return {"Status": True, "Message": "Cliente cadastrado com sucesso!"}

    def creat_account(self, name: str, cpf: str, date_of_birth: str, password: str, balance: int = 0):
        
        account_number = self._accounts.__len__() + 1

        while self._research_account(account_number):
            account_number += 1
        
        result = self._creat_user(name, cpf, date_of_birth)

        if not result["Status"]:
            return result

        new_account = Account(self._clients[cpf], account_number, balance, password)

        self._accounts[account_number] = new_account

        return {"Status": True, "Message": "Conta criada com sucesso!", "info": new_account}

    def _del_client(self, cpf: str):
        if not self._research_client(cpf):
            return {"Status": False, "Message": "Cliente não encontrado"}
        
        del self._clients[cpf]

        return {"Status": True, "Message": "Cliente deletado com sucesso!"}
    
    def del_account(self, account_number: int):
        if not self._research_account(account_number):
            return {"Status": False, "Message": "Conta não encontrada"}
        
        if not self._del_client(self._accounts[account_number].cliente.cpf)["Status"]:
            return {"Status": False, "Message": "Erro ao deletar cliente"}
        
        del self._accounts[account_number]

        return {"Status": True, "Message": "Conta deletada com sucesso!"}
    
    def log_in_account(self, account_number: int, password: str):
        if not self._research_account(account_number):
            return {"Status": False, "Message": "Conta não encontrada"}
        
        account = self._accounts[account_number]

        if account.password != password:
            return {"Status": False, "Message": "Senha incorreta!"}
        
        return AccountService(account)
