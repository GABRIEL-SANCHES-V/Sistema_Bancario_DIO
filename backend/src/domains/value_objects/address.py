from domains.value_objects.zip_code import ZipCode
from domains.value_objects.state import State
from domains.exceptions import (
    AddressError,
    AddressInvalidTypeStateError,
    AddressInvalidTypeZipCodeError,
    AddressInvalidTypeError,
    AddressInvalidValueError,
    StateError,
    ZipCodeError,
)


class Address:
    """
        Value Object que representa um endereço, composto por rua, número, complemento, bairro, cidade, estado, CEP e país.

        O endereço é imutável e possui validações para garantir a integridade dos dados. Ele também possui um método de formatação para exibir o endereço de forma legível.

        Características:
        - Imutável: uma vez criado, o endereço não pode ser alterado.
        - Validações: o construtor valida os tipos e valores dos campos, garantindo que o endereço seja sempre válido.
        - Formatação: o método `formatted` retorna uma string formatada do endereço, facilitando a exibição em interfaces de usuário ou relatórios.
        - Uso em sets e como chave de dicionário: o método `__hash__` permite que o endereço seja usado em sets e como chave de dicionário, garantindo que endereços iguais sejam tratados como iguais.
    """

    __slots__ = (
        "_street",
        "_number",
        "_complement",
        "_neighborhood",
        "_city",
        "_state",
        "_zip_code",
        "_country",
    )

    def __init__(
        self,
        street: str,
        number: str,
        neighborhood: str,
        city: str,
        state: State,
        zip_code: ZipCode,
        country: str = "Brasil",
        complement: str | None = None,
    ):

        if not isinstance(state, State):
            raise AddressInvalidTypeStateError(type(state), State)

        if not isinstance(zip_code, ZipCode):
            raise AddressInvalidTypeZipCodeError(type(zip_code), ZipCode)

        street = self._normalize_string(street, "street")
        number = number.strip() if isinstance(number, str) else str(number)
        neighborhood = self._normalize_string(neighborhood, "neighborhood")
        city = self._normalize_string(city, "city")
        country = self._normalize_string(country, "country")
        complement = self._normalize_string(complement, "complement") if complement else None

        self._validate_required_fields(
            street,
            number,
            neighborhood,
            city,
            country,
        )

        object.__setattr__(self, "_street", street)
        object.__setattr__(self, "_number", number)
        object.__setattr__(self, "_complement", complement)
        object.__setattr__(self, "_neighborhood", neighborhood)
        object.__setattr__(self, "_city", city)
        object.__setattr__(self, "_state", state)
        object.__setattr__(self, "_zip_code", zip_code)
        object.__setattr__(self, "_country", country)

    # ---------------------------------------------------------------
    # Propriedades
    # ---------------------------------------------------------------

    @property
    def street(self) -> str:
        return self._street

    @property
    def number(self) -> str:
        return self._number

    @property
    def complement(self) -> str | None:
        return self._complement

    @property
    def neighborhood(self) -> str:
        return self._neighborhood

    @property
    def city(self) -> str:
        return self._city

    @property
    def state(self) -> State:
        return self._state

    @property
    def state_formatted(self) -> str:
        return self._state.formatted

    @property
    def zip_code(self) -> ZipCode:
        return self._zip_code

    @property
    def zip_code_formatted(self) -> str:
        return self._zip_code.formatted

    @property
    def country(self) -> str:
        return self._country

    @property
    def formatted(self) -> str:
        comp = f" - {self.complement}" if self.complement else ""

        return (
            f"{self.street}, {self.number}{comp} - {self.neighborhood}\n"
            f"{self.city} - {self.state_formatted} - {self.country}\n"
            f"{self.zip_code_formatted}"
        )

    # ---------------------------------------------------------------
    # Validação pública
    # ---------------------------------------------------------------

    @classmethod
    def is_valid(
        cls,
        street: str,
        number: str,
        neighborhood: str,
        city: str,
        state: State,
        zip_code: ZipCode,
        country: str = "Brasil",
    ) -> bool:

        try:
            cls(
                street,
                number,
                neighborhood,
                city,
                state,
                zip_code,
                country,
            )
            return True
        except (AddressError, StateError, ZipCodeError):
            return False

    # ---------------------------------------------------------------
    # Normalização
    # ---------------------------------------------------------------

    @staticmethod
    def _normalize_string(value: str, field_name: str) -> str:

        if not isinstance(value, str):
            raise AddressInvalidTypeError(field_name, type(value), str)

        return value.strip().title()

    # ---------------------------------------------------------------
    # Validação de campos obrigatórios
    # ---------------------------------------------------------------

    @staticmethod
    def _validate_required_fields(
        street: str,
        number: str,
        neighborhood: str,
        city: str,
        country: str,
    ):

        if not street:
            raise AddressInvalidValueError("street", street)

        if not number:
            raise AddressInvalidValueError("number", number)

        if not neighborhood:
            raise AddressInvalidValueError("neighborhood", neighborhood)

        if not city:
            raise AddressInvalidValueError("city", city)

        if not country:
            raise AddressInvalidValueError("country", country)

    # ---------------------------------------------------------------
    # Igualdade
    # ---------------------------------------------------------------

    def __eq__(self, other) -> bool:

        if not isinstance(other, Address):
            return NotImplemented

        return (
            self._street == other._street
            and self._number == other._number
            and self._complement == other._complement
            and self._neighborhood == other._neighborhood
            and self._city == other._city
            and self._state == other._state
            and self._zip_code == other._zip_code
            and self._country == other._country
        )

    # ---------------------------------------------------------------
    # Hash
    # ---------------------------------------------------------------

    def __hash__(self) -> int:

        return hash(
            (
                self._street,
                self._number,
                self._complement,
                self._neighborhood,
                self._city,
                self._state,
                self._zip_code,
                self._country,
            )
        )

    # ---------------------------------------------------------------
    # Representação
    # ---------------------------------------------------------------

    def __str__(self) -> str:
        return self.formatted

    def __repr__(self) -> str:
        return (
            f"Address("
            f"street={self.street!r}, "
            f"number={self.number!r}, "
            f"complement={self.complement!r}, "
            f"neighborhood={self.neighborhood!r}, "
            f"city={self.city!r}, "
            f"state={self.state!r}, "
            f"zip_code={self.zip_code!r}, "
            f"country={self.country!r})"
        )

    # ---------------------------------------------------------------
    # Imutabilidade
    # ---------------------------------------------------------------

    def __setattr__(self, key, value):
        raise AddressError("Address é imutável")