from domains.exceptions.domain_errors import DomainError

class EmailError(DomainError):
    pass

class EmailInvalidTypeError(EmailError):
    def __init__(self, received_type: str):
        super().__init__(f"Email deve ser uma string. Tipo recebido: {received_type}")