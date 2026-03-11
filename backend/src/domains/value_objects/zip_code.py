from domains.exceptions import (
    ZipCodeError,
    ZipCodeInvalidTypeError,
    ZipCodeInvalidFormatError,
)
import re

_RE_ZIP_CODE = re.compile(r"\D")


class ZipCode:

    __slots__ = ("_value",)

    def __init__(self, value: str):

        value = self._normalize(value)
        self._validate_zip_code(value)

        object.__setattr__(self, "_value", value)

    # -----------------------------
    # Propriedades
    # -----------------------------

    @property
    def value(self) -> str:
        return self._value

    @property
    def formatted(self) -> str:
        return f"{self._value[:5]}-{self._value[5:]}"


    # -----------------------------
    # Validação pública
    # -----------------------------

    @classmethod
    def is_valid(cls, value: str) -> bool:
        try:
            cls(value)
            return True
        except ZipCodeError:
            return False


    # -----------------------------
    # Normalização
    # -----------------------------

    @staticmethod
    def _normalize(value: str) -> str:

        if not isinstance(value, str):
            raise ZipCodeInvalidTypeError(type(value))

        digits = _RE_ZIP_CODE.sub("", value)

        return digits


    # -----------------------------
    # Validação
    # -----------------------------

    @staticmethod
    def _validate_zip_code(value: str) -> None:

        if len(value) != 8:
            raise ZipCodeInvalidFormatError(value)


    # -----------------------------
    # Igualdade
    # -----------------------------

    def __eq__(self, other):

        if isinstance(other, ZipCode):
            return self._value == other._value
        
        return NotImplemented


    # -----------------------------
    # Hash
    # -----------------------------

    def __hash__(self):
        return hash(self._value)


    # -----------------------------
    # Representação
    # -----------------------------

    def __str__(self):
        return self.formatted


    def __repr__(self):
        return f"ZipCode('{self.formatted}')"


    # -----------------------------
    # Imutabilidade
    # -----------------------------

    def __setattr__(self, key, value):
        raise ZipCodeError("ZipCode é imutável")