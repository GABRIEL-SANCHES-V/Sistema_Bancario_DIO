from domains.exceptions import DomainError

class ClientError(DomainError):
    pass

class ClientAttributeError(ClientError):

    def __init__(self, received_key: str):
        self.received_key = received_key
        super().__init__(
            f"O atributo '{self.received_key}' é imutável e não pode ser alterado após a criação do objeto Client"
        )