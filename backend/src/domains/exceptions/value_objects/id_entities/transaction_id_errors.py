from domains.exceptions.domain_errors import DomainError

class TransactionIdError(DomainError):
    pass

class TransactionIdInvalidTypeError(TransactionIdError):
    def __init__(self, receive_value):
        super().__init__(f"TransactionId deveria ser do tipo UUID, str ou None, mas recebeu {type(receive_value).__name__}")