from ..domain_errors import DomainError

class ZipCodeError(DomainError):
    pass

class ZipCodeInvalidTypeError(ZipCodeError):
    def __init__(self, received_type: type):
        super().__init__(f"CEP deve ser uma string, mas recebeu um valor do tipo {received_type.__name__}.")

class ZipCodeInvalidFormatError(ZipCodeError):
    def __init__(self, value: str):
        super().__init__(f"CEP '{value}' tem formato inválido. O CEP deve conter exatamente 8 dígitos numéricos.")