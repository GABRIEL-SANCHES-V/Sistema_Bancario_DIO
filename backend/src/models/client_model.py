from datetime import datetime

class Client:
    """
        Represents a bank client.

        Attributes:
            name (str): Client's full name.
            cpf (str): Client's CPF (Brazilian ID).
            date_of_birth (date): Client's birth date.
            age (int): Client's age.
    """
    def __init__(self, name: str, cpf: str, date_of_birth: datetime.date):
        self._name = name
        self._cpf = cpf
        self._date_of_birth = date_of_birth

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def cpf(self) -> str:
        return self._cpf

    @cpf.setter
    def cpf(self, cpf: str):
        self._cpf = cpf

    @property
    def date_of_birth(self) -> datetime.date:
        return self._date_of_birth
    
    @date_of_birth.setter
    def date_of_birth(self, date_of_birth: datetime.date):
        self._date_of_birth = date_of_birth

    @property
    def age(self) -> int:
        today = datetime.today().date()
        return (
            today.year
            - self._date_of_birth.year
            - ((today.month, today.day) < (self._date_of_birth.month, self._date_of_birth.day))
        )
    