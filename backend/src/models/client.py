from datetime import datetime

class Client:
    """
        Represents a bank client.

        Attributes:
            name (str): Client's full name.
            cpf (str): Client's CPF (Brazilian ID).
            date_of_birth (date): Client's birth date.
    """
    def __init__(self, name: str, cpf: str, date_of_birth: str):
        self._name = name
        self._cpf = cpf
        self._date_of_birth = datetime.strptime(date_of_birth, "%d/%m/%Y").date()

    def __str__(self):
        return f'{"Dados do Cliente".center(50, "-")} \nNome: {self.name}\nCPF: {self.cpf}\nData de Nascimento: {self.date_of_birth}'
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, cpf: str):
        self._cpf = cpf

    @property
    def date_of_birth(self):
        return self._date_of_birth.strftime("%d/%m/%Y")
    
    @date_of_birth.setter
    def date_of_birth(self, date_of_birth: str):
        self._date_of_birth = datetime.strptime(date_of_birth, "%d/%m/%Y").date()

    @property
    def age(self):
        today = datetime.today().date()
        return (
            today.year
            - self._date_of_birth.year
            - ((today.month, today.day) < (self._date_of_birth.month, self._date_of_birth.day))
        )
    