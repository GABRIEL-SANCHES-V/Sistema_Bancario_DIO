from ..domain_errors import DomainError

class StateError(DomainError):
    pass

class StateInvalidTypeError(StateError):
    def __init__(self, received_type: type):
        super().__init__(f"Estado deve ser uma string, mas recebeu um valor do tipo {received_type.__name__}.")

class StateInvalidError(StateError):
    def __init__(self, value: str):
        super().__init__(f"Estado '{value}' não é valido.")