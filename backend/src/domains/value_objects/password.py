from domains.exceptions import (
    PasswordError,
    PasswordInvalidTypeError,
    PasswordTooShortError,
    PasswordMissingUppercaseError,
    PasswordMissingLowercaseError,
    PasswordMissingNumberError,
    PasswordMissingSymbolError,
)
import bcrypt
import re

_MIN_LENGTH = 8
_RE_UPPER = re.compile(r"[A-Z]")
_RE_LOWER = re.compile(r"[a-z]")
_RE_NUMBER = re.compile(r"\d")
_RE_SYMBOL = re.compile(r"[!@#$%^&*()]")
_ROUNDS = 4

class Password:
    """
        Value Object para representar uma senha segura.
        
        Este Objeto encapsula a lógica de validação, hashing e verificação de senhas.
        Ele é imutável após a criação, garantindo que o valor da senha não possa ser alterado.

        Características:
            - Valida a senha com regras de complexidade (tamanho, tipos de caracteres)
            - Armazena apenas o hash da senha, nunca o texto plano
            - Fornece um método para verificar se uma senha em texto plano corresponde ao hash armazenado
            - Garante imutabilidade após a criação
    """
    
    __slots__ = ('_hashed_password',)

    def __init__(self, plain_password: str) -> None:

        self._validate_password(plain_password)

        hashed = bcrypt.hashpw(
            plain_password.encode('utf-8'), 
            bcrypt.gensalt(rounds=_ROUNDS)
        )

        object.__setattr__(self, '_hashed_password', hashed)
    

    # ---------------------------------------------------------------
    # Propriedades
    # ---------------------------------------------------------------

    @property
    def hashed_password(self) -> str:
        return self._hashed_password.decode('utf-8')
    

    #---------------------------------------------------------------
    # Verificação de senha
    #---------------------------------------------------------------

    def verify(self, plain_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            self._hashed_password
        )


    #---------------------------------------------------------------
    # Fábrica para criar um Password a partir de um hash existente
    #---------------------------------------------------------------

    @classmethod
    def from_hash(cls, hashed_password: str):

        obj = cls.__new__(cls)

        object.__setattr__(
            obj,
            "_hashed_password",
            hashed_password.encode()
        )

        return obj
    
    #---------------------------------------------------------------
    # Validação
    #---------------------------------------------------------------

    def _validate_password(self, plain_password: str) -> None:
        if not isinstance(plain_password, str):
            raise PasswordInvalidTypeError(type(plain_password))
        
        if len(plain_password) < _MIN_LENGTH:
            raise PasswordTooShortError(len(plain_password))
        
        if not _RE_UPPER.search(plain_password):
            raise PasswordMissingUppercaseError()
        
        if not _RE_LOWER.search(plain_password):
            raise PasswordMissingLowercaseError()
        
        if not _RE_NUMBER.search(plain_password):
            raise PasswordMissingNumberError()
        
        if not _RE_SYMBOL.search(plain_password):
            raise PasswordMissingSymbolError()


    #---------------------------------------------------------------
    # Representação
    #---------------------------------------------------------------

    def __repr__(self) -> str:
        return f"<Password: *****>"
    

    #---------------------------------------------------------------
    # Imutabilidade
    #---------------------------------------------------------------
    def __setattr__(self, key, value):
        raise PasswordError("Password é um objeto imutável. Não é possível alterar o valor depois de criado.")