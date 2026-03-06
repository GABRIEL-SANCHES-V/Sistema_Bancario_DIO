import re

from domains.exceptions import *

#Regex fora da classe para evitar recompilação a cada instância criada, já que é imutável e pode ser reutilizada
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

    Exemplo:
        >>> cpf = CPF("123.456.789-09")
        >>> print(cpf)
        123.456.789-09
        >>> cpf.value
        '12345678909'
    """

    #Foi feito para limita os atributos para economizar memória e reforçar a imutabilidade
    __slots__ = ("_value",)

    def __init__(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("CPF deve ser fornecido como string")
        
        value_normalized = self._normalized_cpf(value)
        
        self._validate_cpf(value_normalized)

        #Burla a imutabilidade para definir o valor após validação, mas só dentro do constructor
        object.__setattr__(self, "_value", value_normalized)


    @property
    def value(self) -> str:
        return self._value
    

    def formatted(self) -> str:
        cpf = self._value
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    

    #---------------------------------------------------------------
    # Normalização: remove caracteres não numéricos para validação
    #---------------------------------------------------------------
    @staticmethod
    def _normalized_cpf(value: str) -> str:
        return _NON_DIGIT_RE.sub("", value)
    
    
    #---------------------------------------------------------------
    # Validação: regras específicas do CPF (tamanho, dígitos, etc)
    #---------------------------------------------------------------
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
    # Igualdade: compara o valor do CPF, não a identidade do objeto
    #---------------------------------------------------------------
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CPF):
            return NotImplemented
        return self._value == other._value
    


    #----------------------------------------------------
    # Hash: permite uso em sets e como chave de dicionário
    #----------------------------------------------------
    def __hash__(self) -> int:
        return hash(self._value)
    

    #----------------------------------------------------
    # Representação: string formatada para exibição
    #----------------------------------------------------
    def __str__(self) -> str:
        return self.formatted()
    

    def __repr__(self) -> str:
        return f"CPF('{self._value}')"
    

    #----------------------------------------------------
    # Imutabilidade: impede alterações após criação
    #----------------------------------------------------
    def __setattr__(self, key: str, value: object) -> None:
        raise AttributeError("CPF é um objeto imutável")