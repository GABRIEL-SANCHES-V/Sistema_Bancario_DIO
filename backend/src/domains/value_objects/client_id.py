from domains.exceptions import (
    ClientIdError,
    ClientIdInvalidTypeError,
)
import uuid


class ClientID:

    __slots__ = ("_value",)

    def __init__(self, value: uuid.UUID | str | None = None):

        if value is None:
            value = uuid.uuid4()

        elif isinstance(value, str):
            value = uuid.UUID(value)

        elif not isinstance(value, uuid.UUID):
            raise ClientIdInvalidTypeError(value)

        object.__setattr__(self, "_value", value)

    # ---------------------------------------------------------------
    # Propriedades
    # ---------------------------------------------------------------

    @property
    def value(self) -> uuid.UUID:
        return self._value

    @property
    def hex(self) -> str:
        return self._value.hex

    # ---------------------------------------------------------------
    # Representação
    # ---------------------------------------------------------------

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self._value}')"

    # ---------------------------------------------------------------
    # Igualdade
    # ---------------------------------------------------------------

    def __eq__(self, other):

        if not isinstance(other, self.__class__):
            return False

        return self._value == other._value

    # ---------------------------------------------------------------
    # Hash
    # ---------------------------------------------------------------

    def __hash__(self):
        return hash(self._value)

    # ---------------------------------------------------------------
    # Imutabilidade
    # ---------------------------------------------------------------

    def __setattr__(self, key, value):
        raise ClientIdError(
            f"{self.__class__.__name__} é imutável e não pode ser modificado."
        )