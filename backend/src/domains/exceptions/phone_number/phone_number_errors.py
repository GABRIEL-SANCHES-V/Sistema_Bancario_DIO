from ..domain_errors import DomainError

class PhoneNumberError(DomainError):
    """Classe base para exceções relacionadas a PhoneNumber."""
    pass


class PhoneNumberInvalidLengthError(PhoneNumberError):
    """Exceção lançada quando o número de telefone não possui 11 dígitos."""
    def __init__(self, length: int) -> None:
        self.length = length
        super().__init__(f"Número de telefone deve conter 11 dígitos (DDD + número). Recebido: {length}")


class PhoneNumberInvalidTypeError(PhoneNumberError):
    """Exceção lançada quando o valor fornecido para o número de telefone não é uma string."""
    def __init__(self, value_type: type) -> None:
        self.value_type = value_type
        super().__init__(f"Número de telefone deve ser fornecido como string. Tipo recebido: {value_type.__name__}")


class PhoneNumberMissingDigitError(PhoneNumberError):
    """Exceção lançada quando o número de telefone não possui o dígito 9 obrigatório para celulares."""
    def __init__(self) -> None:
        super().__init__("Número de telefone celular deve conter o dígito 9 após o DDD.")


class PhoneNumberInvalidDDDError(PhoneNumberError):
    """Exceção lançada quando o DDD do número de telefone é inválido."""
    def __init__(self, ddd: str) -> None:
        self.ddd = ddd
        super().__init__(f"DDD inválido: {ddd}. DDD deve conter 2 dígitos e ser válido no Brasil.")