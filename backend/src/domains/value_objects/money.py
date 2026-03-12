from decimal import Decimal, ROUND_HALF_UP
from domains.exceptions import (
    MoneyError,
    MoneyInvalidTypeError,
    MoneyInvalidValueError,
)


class Money:

    __slots__ = ("_amount",)

    def __init__(self, amount: Decimal | int | str):

        amount = self._normalize(amount)
        self._validate(amount)

        object.__setattr__(self, "_amount", amount)

    # ---------------------------------------------------------------
    # Propriedades
    # ---------------------------------------------------------------

    @property
    def amount(self) -> Decimal:
        return self._amount

    # ---------------------------------------------------------------
    # Normalização
    # ---------------------------------------------------------------

    @staticmethod
    def _normalize(value) -> Decimal:
        try:
            amount = Decimal(value)
        except Exception:
            raise MoneyInvalidTypeError(type(value), (Decimal, int, str))

        return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # ---------------------------------------------------------------
    # Validação
    # ---------------------------------------------------------------

    @staticmethod
    def _validate(value: Decimal):

        if value < 0:
            raise MoneyInvalidValueError("amount", value)

    # ---------------------------------------------------------------
    # Operações
    # ---------------------------------------------------------------

    def add(self, other: "Money") -> "Money":

        if not isinstance(other, Money):
            raise MoneyInvalidTypeError(type(other), Money)

        return Money(self._amount + other._amount)

    def subtract(self, other: "Money") -> "Money":

        if not isinstance(other, Money):
            raise MoneyInvalidTypeError(type(other), Money)

        result = self._amount - other._amount

        if result < 0:
            raise MoneyInvalidValueError("amount", result)

        return Money(result)

    # ---------------------------------------------------------------
    # Comparações
    # ---------------------------------------------------------------

    def __eq__(self, other):

        if not isinstance(other, Money):
            return NotImplemented

        return self._amount == other._amount

    def __lt__(self, other):

        if not isinstance(other, Money):
            return NotImplemented

        return self._amount < other._amount

    def __le__(self, other):

        if not isinstance(other, Money):
            return NotImplemented

        return self._amount <= other._amount

    def __gt__(self, other):

        if not isinstance(other, Money):
            return NotImplemented

        return self._amount > other._amount

    def __ge__(self, other):

        if not isinstance(other, Money):
            return NotImplemented

        return self._amount >= other._amount

    # ---------------------------------------------------------------
    # Hash
    # ---------------------------------------------------------------

    def __hash__(self):

        return hash(self._amount)

    # ---------------------------------------------------------------
    # Representação
    # ---------------------------------------------------------------

    def __str__(self):

        return f"R$ {self._amount}"

    def __repr__(self):

        return f"Money('{self._amount}')"

    # ---------------------------------------------------------------
    # Imutabilidade
    # ---------------------------------------------------------------

    def __setattr__(self, key, value):

        raise MoneyError("Money é imutável")