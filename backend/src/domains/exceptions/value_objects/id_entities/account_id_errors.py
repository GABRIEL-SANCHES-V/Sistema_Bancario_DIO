from domains.exceptions.domain_errors import DomainError

class AccountIdError(DomainError):
    pass

class AccountIdInvalidTypeError(AccountIdError):
    def __init__(self, receive_value):
        super().__init__(f"AccountId deveria ser do tipo UUID, str ou None, mas recebeu {type(receive_value).__name__}")