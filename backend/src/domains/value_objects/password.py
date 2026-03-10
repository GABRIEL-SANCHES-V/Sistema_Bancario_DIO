import bcrypt
import re

_MIN_LENGTH = 8
_RE_UPPER = re.compile(r"[A-Z]")
_RE_LOWER = re.compile(r"[a-z]")
_RE_NUMBER = re.compile(r"\d")
_RE_SYMBOL = re.compile(r"[!@#$%^&*()]")
_ROUNDS = 12

class Password:
    
    __slots__ = ('_hashed_password',)

    def __init__(self, plain_password: str) -> None:

        self._validate_password(plain_password)

        hashed = bcrypt.hashpw(
            plain_password.encode('utf-8'), 
            bcrypt.gensalt(rounds=_ROUNDS)
        )

        object.__setattr__(self, '_hashed_password', hashed)
    

    #---------------------------------------------------------------
    # Propriedades para acessar o hash e verificar a senha
    #---------------------------------------------------------------
    @property
    def hashed_password(self) -> str:
        return self._hashed_password.decode('utf-8')

    @property
    def verify(self) -> bool:
        return bcrypt.checkpw(
            self._plain_password.encode('utf-8'),
            self._hashed_password
        )
    

    #---------------------------------------------------------------
    # Validação: regras de complexidade da senha
    #---------------------------------------------------------------
    def _validate_password(self, plain_password: str) -> None:
        if not isinstance(plain_password, str):
            raise TypeError("Senha deve ser uma string.")
        
        if len(plain_password) < _MIN_LENGTH:
            raise ValueError(f"Senha deve ter pelo menos {_MIN_LENGTH} caracteres.")
        
        if not _RE_UPPER.search(plain_password):
            raise ValueError("Senha deve conter pelo menos uma letra maiúscula.")
        
        if not _RE_LOWER.search(plain_password):
            raise ValueError("Senha deve conter pelo menos uma letra minúscula.")
        
        if not _RE_NUMBER.search(plain_password):
            raise ValueError("Senha deve conter pelo menos um número.")
        
        if not _RE_SYMBOL.search(plain_password):
            raise ValueError("Senha deve conter pelo menos um caractere especial.")
        

    #---------------------------------------------------------------
    # Representação para debugging (não mostra a senha real)
    #---------------------------------------------------------------
    def __repr__(self) -> str:
        return f"<Password: *****>"
    

    #---------------------------------------------------------------
    # Fábrica para criar um Password a partir de um hash existente (ex: do banco)
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
    # Imutabilidade: não permite alterar o hash depois de criado
    #---------------------------------------------------------------
    def __setattr__(self, key, value):
        if hasattr(self, '_hashed_password'):
            raise AttributeError("Password é um objeto imutável.")
        super().__setattr__(key, value)