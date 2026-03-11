import re


_RE_ZIP_CODE = re.compile(r"\D")


DICT_UF = {
    "AC": "Acre",
    "AL": "Alagoas",
    "AP": "Amapá",
    "AM": "Amazonas",
    "BA": "Bahia",
    "CE": "Ceará",
    "DF": "Distrito Federal",
    "ES": "Espírito Santo",
    "GO": "Goiás",
    "MA": "Maranhão",
    "MT": "Mato Grosso",
    "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais",
    "PA": "Pará",
    "PB": "Paraíba",
    "PR": "Paraná",
    "PE": "Pernambuco",
    "PI": "Piauí",
    "RJ": "Rio de Janeiro",
    "RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul",
    "RO": "Rondônia",
    "RR": "Roraima",
    "SC": "Santa Catarina",
    "SP": "São Paulo",
    "SE": "Sergipe",
    "TO": "Tocantins",
}


class Address:

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
        state: str,
        zip_code: str,
        country: str = "Brasil",
        complement: str | None = None,
    ):

        street = self._normalize_string(street)
        number = number.strip()
        neighborhood = self._normalize_string(neighborhood)
        city = self._normalize_string(city)
        state = state.strip().upper()
        zip_code = self._normalize_zip_code(zip_code)
        country = self._normalize_string(country)
        complement = self._normalize_string(complement) if complement else None

        self._validate_required_fields(
            street,
            number,
            neighborhood,
            city,
            state,
            zip_code,
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
    # Propriedades (imutáveis)
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
    def state(self) -> str:
        return self._state

    @property
    def zip_code(self) -> str:
        return self._zip_code
    
    @property
    def zip_code_formatted(self) -> str:
        return f"{self._zip_code[:5]}-{self._zip_code[5:]}"

    @property
    def country(self) -> str:
        return self._country

    @property
    def formatted(self) -> str:
        comp = f" - {self.complement}" if self.complement else ""

        return (
            f"{self.street}, {self.number}{comp} - {self.neighborhood}\n"
            f"{self.city} - {self.state} - {self.country}\n"
            f"{self.zip_code_formatted}"
        )
            

    # ----------------------------------------------------------------
    # Validação: método público para verificar se um endereço é válido
    # ----------------------------------------------------------------

    @classmethod
    def is_valid(
        cls,
        street: str,
        number: str,
        neighborhood: str,
        city: str,
        state: str,
        zip_code: str,
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
        except ValueError:
            return False


    # ---------------------------------------------------------------
    # Normalização
    # ---------------------------------------------------------------

    @staticmethod
    def _normalize_string(value: str) -> str:
        if not isinstance(value, str):
            ValueError("Valor deve ser uma string")
        return value.strip().title()

    @staticmethod
    def _normalize_zip_code(value: str) -> str:
        zip_code = _RE_ZIP_CODE.sub("", value)

        if len(zip_code) != 8:
            raise ValueError("CEP inválido")

        return zip_code


    # ---------------------------------------------------------------
    # Validação de campos obrigatórios
    # ---------------------------------------------------------------

    @staticmethod
    def _validate_required_fields(
        street,
        number,
        neighborhood,
        city,
        state,
        zip_code,
        country,
    ):
        if not street:
            raise ValueError("Rua é obrigatória")

        if not number:
            raise ValueError("Número é obrigatório")

        if not neighborhood:
            raise ValueError("Bairro é obrigatório")

        if not city:
            raise ValueError("Cidade é obrigatória")

        if not state:
            raise ValueError("Estado é obrigatório")

        if not zip_code:
            raise ValueError("CEP é obrigatório")

        if not country:
            raise ValueError("País é obrigatório")
        

    # ---------------------------------------------------------------
    # Igualdade: comparação baseada no valor dos campos
    # ---------------------------------------------------------------

    def __eq__(self, other) -> bool:
        if isinstance(other, Address):
            return (
                self._street == other._street and
                self._number == other._number and
                self._complement == other._complement and
                self._neighborhood == other._neighborhood and
                self._city == other._city and
                self._state == other._state and
                self._zip_code == other._zip_code and
                self._country == other._country
            )
    
        return NotImplemented


    # ---------------------------------------------------------------
    # Hash: permite uso em sets e como chave de dicionário
    # ---------------------------------------------------------------

    def __hash__(self) -> int:
        return hash((
            self.street,
            self.number,
            self.complement,
            self.neighborhood,
            self.city,
            self.state,
            self.zip_code,
            self.country
        ))

    
    # ---------------------------------------------------------------
    # Representação: string formatada para exibição
    # ---------------------------------------------------------------

    def __str__(self) -> str:
        return self.formatted

    def __repr__(self):
        return (
            f"Address(street={self.street!r}, "
            f"number={self.number!r}, "
            f"complement={self.complement!r}, "
            f"neighborhood={self.neighborhood!r}, "
            f"city={self.city!r}, "
            f"state={self.state!r})"
            f"zip_code={self.zip_code!r}, "
            f"country={self.country!r})"
        )


    # ---------------------------------------------------------------
    # Imutabilidade: não expõe setters
    # ---------------------------------------------------------------

    def __setattr__(self, key, value):
        raise AttributeError("Address é imutável")
