from domains.exceptions.domain_errors import DomainError

class PasswordError(DomainError):
    pass

class PasswordInvalidTypeError(PasswordError):
    def __init__(self, received_type: type):
        super().__init__(f"Senha deve ser uma string. Tipo recebido: {received_type.__name__}")

class PasswordTooShortError(PasswordError):
    def __init__(self, min_length: int):
        super().__init__(f"Senha deve ter pelo menos {min_length} caracteres.")
    
class PasswordMissingUppercaseError(PasswordError):
    def __init__(self):
        super().__init__("Senha deve conter pelo menos uma letra maiúscula.")

class PasswordMissingLowercaseError(PasswordError):
    def __init__(self):
        super().__init__("Senha deve conter pelo menos uma letra minúscula.")

class PasswordMissingNumberError(PasswordError):
    def __init__(self):
        super().__init__("Senha deve conter pelo menos um número.")

class PasswordMissingSymbolError(PasswordError):
    def __init__(self):
        super().__init__("Senha deve conter pelo menos um caractere especial.")