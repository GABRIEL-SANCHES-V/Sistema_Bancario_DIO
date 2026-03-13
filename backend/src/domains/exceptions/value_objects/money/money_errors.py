from domains.exceptions.domain_errors import DomainError

class MoneyError(DomainError):
    pass

class MoneyInvalidTypeError(MoneyError):
    def __init__(self, value_type, expected_types):
        self.value_type = value_type
        self.expected_types = expected_types
        super().__init__(f"Tipo inválido: {value_type}. Esperado: {expected_types}.")

class MoneyInvalidValueError(MoneyError):
    def __init__(self, field_name, value):
        self.field_name = field_name
        self.value = value
        super().__init__(f"Valor inválido para '{field_name}': {value}.")