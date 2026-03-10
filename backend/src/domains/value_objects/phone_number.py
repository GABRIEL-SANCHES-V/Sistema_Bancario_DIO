import re
from domains.exceptions import (
    PhoneNumberError,
    PhoneNumberInvalidLengthError,
    PhoneNumberInvalidTypeError,
    PhoneNumberMissingDigitError,
    PhoneNumberInvalidDDDError,
)


_NON_DIGIT_RE = re.compile(r"\D")

VALID_DDDS = {"11", "12", "13", "14", "15", "16", "17", "18", "19",
                   "21", "22", "24", "27", "28",
                   "31", "32", "33", "34", "35", "37", "38",
                   "41", "42", "43", "44", "45", "46",
                   "47", "48", "49",
                   "51", "53", "54", "55",
                   "61", "62", "64",
                   "63",
                   "65",
                   "66",
                   "67",
                   "68",
                   "69",
                   "71", 
                   "73", 
                   "74", 
                   "75", 
                   "77",
                   "79",
                   "81",
                   "82",
                   "83",
                   "84",
                   "85",
                   "86",
                   "87",
                   "88",
                   "89",
                   "91",
                   "92",
                   "93",
                   "94",
                   "95",
                   "96",
                   "97",
                   "98",
                   "99"}

class PhoneNumber:
    """
        Value Object para representar um número de celular válido.
        Este Objeto encapsula a lógica de validação e formatação de um número de celular.
        Ele é imutável após a criação, garantindo que o valor do número não possa ser alterado.

        Características:
        - Validação de comprimento (11 dígitos)
        - Validação de DDD (códigos válidos)
        - Validação do prefixo (deve começar com 9)
        - Formatação automática
        - Máscara para exibição segura
        - Pode ser utilizado em sets e como chave de dicionário
        - Garante imutabilidade após a criação
    """

    __slots__ = ("_value",)

    def __init__(self, value: str):
        if not isinstance(value, str):
            raise PhoneNumberInvalidTypeError(type(value))
        
        normalized = self._normalize_phone_number(value)

        self._validate_phone_number(normalized)

        object.__setattr__(self, "_value", normalized)
    

    @property
    def value(self) -> str:
        return self._value
    
    @property
    def formatted(self) -> str:
        return f"({self._value[:2]}) {self._value[2:7]}-{self._value[7:]}"
    
    @property
    def masked(self) -> str:
        return f"({self._value[:2]}) *****-{self._value[7:]}"
    
    @property
    def ddd(self) -> str:
        return self._value[:2]
    
    @property
    def number(self) -> str:
        return self._value[2:]


    #---------------------------------------------------------------
    # Normalização: remove caracteres não numéricos para validação
    #---------------------------------------------------------------
    @staticmethod
    def _normalize_phone_number(value: str) -> str:
        return _NON_DIGIT_RE.sub("", value)
    

    #---------------------------------------------------------------
    # Validação: método público para verificar se um número de celular é válido
    #---------------------------------------------------------------
    @classmethod
    def is_valid(cls, value: str) -> bool:
        try:
            cls(value)
            return True
        except PhoneNumberError:
            return False

    #---------------------------------------------------------------
    # Validação: regras específicas do número de celular (tamanho, dígito)
    #---------------------------------------------------------------
    @staticmethod
    def _validate_phone_number(value: str) -> None:
        if len(value) != 11:
            raise PhoneNumberInvalidLengthError(length=len(value))
        
        if value[2] != '9':
            raise PhoneNumberMissingDigitError()
        
        ddd = value[:2]
        if ddd not in VALID_DDDS:
            raise PhoneNumberInvalidDDDError(ddd)


    #---------------------------------------------------------------
    # Igualdade: comparação baseada no valor do número de celular
    #---------------------------------------------------------------
    def __eq__(self, other) -> bool:
        if isinstance(other, PhoneNumber):
            return self._value == other._value

        if isinstance(other, str):
            return self._value == self._normalize_phone_number(other)

        return NotImplemented


    #---------------------------------------------------------------
    # Hash: baseado no valor do número de celular para uso em sets e dicionários
    #---------------------------------------------------------------
    def __hash__(self) -> int:
        return hash(self._value)


    #---------------------------------------------------------------
    # Representação: string formatada para facilitar leitura
    #---------------------------------------------------------------
    def __str__(self) -> str:
        return self.formatted
    
    def __repr__(self) -> str:
        return f"PhoneNumber('{self.formatted}')"
    

    #---------------------------------------------------------------
    # Imutabilidade: impede alterações após criação
    #---------------------------------------------------------------
    def __setattr__(self, key, value):
        if hasattr(self, "_value"):
            raise PhoneNumberError("PhoneNumber é um objeto imutável, e não pode ser modificado após a criação.")
        super().__setattr__(key, value)