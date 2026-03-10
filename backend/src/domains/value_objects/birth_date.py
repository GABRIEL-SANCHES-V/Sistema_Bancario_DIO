from domains.exceptions import (
    BirthDateError,
    BirthDateInFutureError,
    BirthDateTooOldError,
    BirthDateInvalidTypeError,
    BirthDateInvalidFormatError,
    BirthDateInvalidValueError,
)
from datetime import date
import re

_RE_DATE_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_RE_DATE_BR = re.compile(r"^\d{2}/\d{2}/\d{4}$")

class BirthDate:

    __slots__ = ("_value",)

    def __init__(self, value: date | str) -> None:
        if not isinstance(value, date):
            if isinstance(value, str):
                value = self._normalize_date_string(value)
            else:
                raise BirthDateInvalidTypeError(type(value))

        self._validate_birth_date(value)

        object.__setattr__(self, "_value", value)


    #--------------------------------------------------------
    # Propriedades para acesso ao valor e formatações comuns
    #--------------------------------------------------------
    @property
    def value(self) -> date:
        return self._value
    
    @property
    def year(self):
        return self._value.year

    @property
    def month(self):
        return self._value.month

    @property
    def day(self):
        return self._value.day
    
    @property
    def formatted_br(self) -> str:
        return self._value.strftime("%d/%m/%Y")
    
    @property
    def formatted_us(self) -> str:
        return self._value.strftime("%Y-%m-%d")

    @property
    def age(self) -> int:
        today = date.today()
        age = today.year - self._value.year
        if (today.month, today.day) < (self._value.month, self._value.day):
            age -= 1
        return age
    
    @property
    def is_adult(self) -> bool:
        return self.age >= 18
    

    #---------------------------------------------------------------
    # Validação: método público para verificar se uma data de nascimento é válida
    #---------------------------------------------------------------
    @classmethod
    def is_valid(cls, value: date | str) -> bool:
        try:
            cls(value)
            return True
        except BirthDateError:
            return False
        
    
    #---------------------------------------------------------------
    # Normalização: método privado para converter strings em objetos date, suportando formatos ISO e BR
    #---------------------------------------------------------------
    @staticmethod
    def _normalize_date_string(value: str) -> date:

        if _RE_DATE_ISO.match(value):
            try:
                return date.fromisoformat(value)
            except ValueError:
                raise BirthDateInvalidValueError(value)

        elif _RE_DATE_BR.match(value):
            day, month, year = value.split("/")
            try:
                return date(int(year), int(month), int(day))
            except ValueError:
                raise BirthDateInvalidValueError(value)

        else:
            raise BirthDateInvalidFormatError(value)

    #---------------------------------------------------------------
    # Validação: Metodo privado para verificar se a data de nascimento é válida (não futura, não muito antiga)
    #---------------------------------------------------------------
    @staticmethod
    def _validate_birth_date(value: date) -> None:
        today = date.today()
        if value > today:
            raise BirthDateInFutureError()
        if (today - value).days > 120 * 365:
            raise BirthDateTooOldError()
    

    #---------------------------------------------------------------
    # Igualdade: comparação baseada no valor da data de nascimento
    #---------------------------------------------------------------
    def __eq__(self, other) -> bool:
        if isinstance(other, BirthDate):
            return self._value == other._value
        
        if isinstance(other, date):
            return self._value == other
        
        return NotImplemented

    
    #---------------------------------------------------------------
    # Hash: baseado no valor da data de nascimento para uso em coleções
    #---------------------------------------------------------------
    def __hash__(self) -> int:
        return hash(self._value)
    

    #---------------------------------------------------------------
    # Representação: string legível para depuração e logs
    #---------------------------------------------------------------
    def __str__(self) -> str:
        return self.formatted_br
    
    def __repr__(self) -> str:
        return f"BirthDate({self._value.isoformat()})"


    #---------------------------------------------------------------
    # Imutabilidade: bloqueia a modificação do valor após a criação
    #---------------------------------------------------------------
    def __setattr__(self, key, value) -> None:
        if hasattr(self, "_value"):
            raise BirthDateError("BirthDate é um objeto imutável, não pode ser modificado.")
        super().__setattr__(key, value)