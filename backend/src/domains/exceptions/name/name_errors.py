from ..domain_errors import DomainError

class NameErrorVO(DomainError):
    pass

class NameInvalidTypeError(NameErrorVO):
    def __init__(self, name):
        self.name = name
        super().__init__(f"Nome deve ser uma string, não {type(name).__name__}.")

class NameTooShortError(NameErrorVO):
    def __init__(self, min_length):
        self.min_length = min_length
        super().__init__(f"Nome deve ter pelo menos {self.min_length} caracteres.")

class NameTooLongError(NameErrorVO):
    def __init__(self, max_length):
        self.max_length = max_length
        super().__init__(f"Nome deve ter no máximo {self.max_length} caracteres.")

class NameInvalidFormatError(NameErrorVO):
    def __init__(self, name):
        self.name = name
        super().__init__(f"Nome não pode conter caracteres especiais ou números. Valor fornecido: '{self.name}'.")