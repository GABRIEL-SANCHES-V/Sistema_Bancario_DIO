from domains.exceptions import (
    NameErrorVO,
    NameInvalidTypeError,
    NameTooShortError,
    NameTooLongError,
    NameInvalidFormatError,
)
import re

_NAME_REGEX = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿ]+(?: [A-Za-zÀ-ÖØ-öø-ÿ]+)*$")

MIN_NAME_LENGTH = 8
MAX_NAME_LENGTH = 100

class Name:

    __slots__ = ("_name",)

    def __init__(self, name: str):
        if not isinstance(name, str):
            raise NameInvalidTypeError(name)

        name_normalized = self._normalize_name(name)

        self._validate_name(name_normalized)

        object.__setattr__(self, "_name", name_normalized)


    # ---------------------------------------------------------------
    # Propriedades
    # ---------------------------------------------------------------

    @property
    def name(self) -> str:
        return self._name


    # ---------------------------------------------------------------
    # Validação Publica
    # ---------------------------------------------------------------

    @classmethod
    def is_valid(cls, name: str) -> bool:
        try:
            cls(name)
            return True
        except NameErrorVO:
            return False


    # ---------------------------------------------------------------
    # Normalização e validação
    # ---------------------------------------------------------------

    def _normalize_name(self, name: str) -> str:
        return name.strip().title()

    def _validate_name(self, name: str):
        if len(name) < MIN_NAME_LENGTH:
            raise NameTooShortError(MIN_NAME_LENGTH)

        if len(name) > MAX_NAME_LENGTH:
            raise NameTooLongError(MAX_NAME_LENGTH)

        if not _NAME_REGEX.match(name):
            raise NameInvalidFormatError(name)


    # ---------------------------------------------------------------
    # Representação
    # ---------------------------------------------------------------

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return f"Name('{self._name}')"
    

    # ---------------------------------------------------------------
    # Igualdade e hash
    # ---------------------------------------------------------------

    def __eq__(self, other) -> bool:
        if isinstance(other, Name):
            return self._name == other._name
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._name)


    # ---------------------------------------------------------------
    # Imutabilidade
    # ---------------------------------------------------------------
    
    def __setattr__(self, key, value):
        raise NameErrorVO("Name é um objeto imutável.")
        
