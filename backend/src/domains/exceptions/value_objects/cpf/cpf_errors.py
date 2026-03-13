from domains.exceptions.domain_errors import DomainError

class CPFError(DomainError):
    """Classe base para erros relacionados ao CPF."""
    pass

class CPFInvalidLengthError(CPFError):
    """Erro para CPF com comprimento inválido."""
    def __init__(self, received_length: int):
        super().__init__(f"CPF deve ter exatamente 11 números, mas recebeu {received_length}.")

class CPFInvalidCheckDigitsError(CPFError):
    def __init__(self):
        super().__init__("Dígitos verificadores do CPF são inválidos.")

class CPFRepeatedDigitsError(CPFError):
    def __init__(self):
        super().__init__("CPF não pode ter todos os dígitos iguais.")

class CPFInvalidTypeError(CPFError):
    def __init__(self, received_type: type):
        super().__init__(f"CPF deve ser uma string, mas recebeu um valor do tipo {received_type.__name__}.")