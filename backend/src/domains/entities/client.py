from domains.value_objects import (
    ClientID,
    Name,
    Email,
    CPF,
    PhoneNumber,
    BirthDate,
    Address
)
from domains.exceptions import ClientAttributeError

class Client:

    __slots__ = (
        '_client_id',
        '_name',
        '_email',
        '_cpf',
        '_phone_number',
        '_birth_date',
        '_address'
    )
    def __init__(
        self,
        name: Name,
        email: Email,
        cpf: CPF,
        phone_number: PhoneNumber,
        birth_date: BirthDate,
        address: Address,
        ):
        self._client_id = ClientID()
        self._name = name
        self._email = email
        self._cpf = cpf
        self._phone_number = phone_number
        self._birth_date = birth_date
        self._address = address


    # ---------------------------------------------------------------
    # Propriedades Imutáveis
    # ---------------------------------------------------------------

    @property
    def client_id(self):
        return self._client_id

    @property
    def cpf(self):
        return self._cpf
    

    # ---------------------------------------------------------------
    # Propriedades Mutáveis
    # ---------------------------------------------------------------
    
    @property
    def name(self):
        return self._name
    
    def change_name(self, new_name: Name):
        if self._name == new_name:
            return
        
        self._name = new_name


    @property
    def email(self):
        return self._email

    def change_email(self, new_email: Email):
        if self._email == new_email:
            return
        
        self._email = new_email


    @property
    def phone_number(self):
        return self._phone_number

    def change_phone_number(self, new_phone_number: PhoneNumber):
        if self._phone_number == new_phone_number:
            return
        
        self._phone_number = new_phone_number


    @property
    def address(self):
        return self._address
    
    def change_address(self, new_address: Address):
        if self._address == new_address:
            return
        
        self._address = new_address

    @property
    def birth_date(self):
        return self._birth_date
    
    def change_birth_date(self, new_birth_date: BirthDate):
        if self._birth_date == new_birth_date:
            return
        
        self._birth_date = new_birth_date

    @property
    def age(self):
        return self._birth_date.age


    #---------------------------------------------------------------
    # Representação
    #---------------------------------------------------------------

    def __str__(self):
        return (
            f"\n{'-'*50}\n"
            f"ID: {self.client_id}\n"
            f"Nome: {self.name} - {self.age} anos\n"
            f"Email: {self.email}\n"
            f"CPF: {self.cpf}\n"
            f"Telefone: {self.phone_number}\n"
            f"Data de Nascimento: {self.birth_date}\n"
            f"Endereço: {self.address}\n"
            f"{'-'*50}"
        )

    def __repr__(self):
        return (
            f"Client(client_id={self.client_id}, name={self.name}, email={self.email}, "
            f"cpf={self.cpf}, phone_number={self.phone_number}, birth_date={self.birth_date}, "
            f"address={self.address})"
        )

    
    #---------------------------------------------------------------
    # Imutabilidade
    #---------------------------------------------------------------
    
    def __setattr__(self, key, value):
        if key in {"_client_id", "client_id", "_cpf", "cpf"} and hasattr(self, key):
            raise ClientAttributeError(key)

        object.__setattr__(self, key, value)
