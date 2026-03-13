import re

from domains.exceptions import (
    CPFError,
    CPFInvalidLengthError,
    CPFInvalidCheckDigitsError,
    CPFRepeatedDigitsError,
    CPFInvalidTypeError,
)

_NON_DIGIT_RE = re.compile(r"\D")

class CPF:
    """
    Value Object que representa um CPF brasileiro válido.

    Esta classe encapsula a lógica de normalização, validação e
    representação de um CPF. O objeto é imutável após sua criação.

    Características:
        - Normaliza entrada removendo caracteres não numéricos
        - Valida comprimento e dígitos verificadores
        - Garante imutabilidade
        - Pode ser utilizado em sets e como chave de dicionário
    """

    __slots__ = ("_value",)

    def __init__(self, value: str) -> None:
        if not isinstance(value, str):
            raise CPFInvalidTypeError(type(value))
        
        value_normalized = self._normalized_cpf(value)
        
        self._validate_cpf(value_normalized)

        object.__setattr__(self, "_value", value_normalized)


    # ---------------------------------------------------------------
    # Propriedades
    # ---------------------------------------------------------------

    @property
    def value(self) -> str:
        return self._value

    @property
    def formatted(self) -> str:
        cpf = self._value
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    
    @property
    def masked(self) -> str:
        cpf = self._value
        return f"{cpf[:3]}.***.***-{cpf[9:]}"
    

    #---------------------------------------------------------------
    # Validação pública
    #---------------------------------------------------------------

    @classmethod
    def is_valid(cls, value: str) -> bool:
        try:
            cls(value)
            return True
        except CPFError:
            return False


    #---------------------------------------------------------------
    # Normalização e Validação
    #---------------------------------------------------------------

    @staticmethod
    def _normalized_cpf(value: str) -> str:
        return _NON_DIGIT_RE.sub("", value)

    @classmethod
    def _validate_cpf(cls, cpf: str) -> None:
        if len(cpf) != 11:
            raise CPFInvalidLengthError(len(cpf))
        
        if len(set(cpf)) == 1:
            raise CPFRepeatedDigitsError()
        
        cls._validate_check_digits(cpf)
    
    @classmethod
    def _validate_check_digits(cls, cpf: str) -> None:
        digits = cpf[:9]

        if cpf[-2:] != cls._calculate_check_digits(digits):
            raise CPFInvalidCheckDigitsError()

    @staticmethod
    def _calculate_check_digits(cpf: str) -> str:

        def calculate_digit(part: str, factor: int) -> str:
            total = sum(int(num) * (factor - i) for i, num in enumerate(part))
            remainder = total % 11
            return "0" if remainder < 2 else str(11 - remainder)

        first = calculate_digit(cpf, 10)
        second = calculate_digit(cpf + first, 11)

        return first + second
    

    #---------------------------------------------------------------
    # Igualdade
    #---------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CPF):
            return self._value == other._value

        if isinstance(other, str):
            return self._value == self._normalized_cpf(other)

        return NotImplemented
        

    #----------------------------------------------------
    # Representação
    #----------------------------------------------------

    def __str__(self) -> str:
        return self.formatted
    

    def __repr__(self) -> str:
        return f"CPF('{self.formatted}')"
    

    #----------------------------------------------------
    # Hash
    #----------------------------------------------------

    def __hash__(self) -> int:
        return hash(self._value)
    

    #----------------------------------------------------
    # Imutabilidade
    #----------------------------------------------------
    
    def __setattr__(self, key: str, value: object) -> None:
        raise CPFError("CPF é um objeto imutável. Não é possível alterar o valor após a criação.")