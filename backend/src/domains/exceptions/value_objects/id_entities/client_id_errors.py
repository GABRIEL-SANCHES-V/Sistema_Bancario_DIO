from domains.exceptions.domain_errors import DomainError

class ClientIdError(DomainError):
    pass

class ClientIdInvalidTypeError(ClientIdError):
    def __init__(self, receive_value):
        super().__init__(f"ClientId deveria ser do tipo UUID, str ou None, mas recebeu {type(receive_value).__name__}")