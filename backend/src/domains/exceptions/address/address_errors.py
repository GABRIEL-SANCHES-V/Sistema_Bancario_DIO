from ..domain_errors import DomainError

class AddressError(DomainError):
    pass

class AddressInvalidTypeStateError(AddressError):
    def __init__(self, received_type: type, expected_type: type):
        super().__init__(f"Tipo de estado inválido: {received_type}, esperado: {expected_type}")

class AddressInvalidTypeZipCodeError(AddressError):
    def __init__(self, received_type: type, expected_type: type):
        super().__init__(f"Tipo de código postal inválido: {received_type}, esperado: {expected_type}")

class AddressInvalidTypeError(AddressError):
    def __init__(self, field_name: str, received_type: type, expected_type: type):
        super().__init__(f"Tipo inválido para {field_name}: {received_type}, esperado: {expected_type}")

class AddressInvalidValueError(AddressError):
    def __init__(self, field_name: str, received_value: str):
        super().__init__(f"Valor inválido para {field_name}: {received_value}")