from ..domain_errors import DomainError


class BirthDateError(DomainError):
    """Exceção para erros relacionados à data de nascimento."""
    pass

class BirthDateInFutureError(BirthDateError):
    """Exceção para data de nascimento no futuro."""
    def __init__(self):
        super().__init__("Data de Nascimento não pode ser no futuro.")

class BirthDateTooOldError(BirthDateError):
    """Exceção para data de nascimento muito antiga."""
    def __init__(self):
        super().__init__("Data de Nascimento não pode ser mais antiga que 120 anos")

class BirthDateInvalidTypeError(BirthDateError):
    """Exceção para tipo inválido de data de nascimento."""
    def __init__(self, received_type: type) -> None:
        self.received_type = received_type
        super().__init__(f"Tipo inválido para Data de Nascimento: {received_type.__name__}. Esperado: date ou string no formato 'YYYY-MM-DD' ou 'DD/MM/YYYY'.")

class BirthDateInvalidFormatError(BirthDateError):
    """Exceção para formato inválido de data de nascimento."""
    def __init__(self, value: str) -> None:
        self.value = value
        super().__init__(f"Formato de Data de Nascimento inválido: '{value}'. Formatos aceitos: 'YYYY-MM-DD' ou 'DD/MM/YYYY'.")

class BirthDateInvalidValueError(BirthDateError):
    """Exceção para valor inválido de data de nascimento."""
    def __init__(self, value: str) -> None:
        self.value = value
        super().__init__(f"Valor de Data de Nascimento inválido: '{value}'. Verifique se a data é válida.")

    