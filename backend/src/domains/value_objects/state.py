from domains.exceptions import (
    StateError,
    StateInvalidTypeError,
    StateInvalidError,
)

DICT_STATES = {
    "Acre": "AC",
    "Alagoas": "AL",
    "Amapá": "AP",
    "Amazonas": "AM",
    "Bahia": "BA",
    "Ceará": "CE",
    "Distrito Federal": "DF",
    "Espírito Santo": "ES",
    "Goiás": "GO",
    "Maranhão": "MA",
    "Mato Grosso": "MT",
    "Mato Grosso Do Sul": "MS",
    "Minas Gerais": "MG",
    "Pará": "PA",
    "Paraíba": "PB",
    "Paraná": "PR",
    "Pernambuco": "PE",
    "Piauí": "PI",
    "Rio De Janeiro": "RJ",
    "Rio Grande Do Norte": "RN",
    "Rio Grande Do Sul": "RS",
    "Rondônia": "RO",
    "Roraima": "RR",
    "Santa Catarina": "SC",
    "São Paulo": "SP",
    "Sergipe": "SE",
    "Tocantins": "TO",
}

DICT_UF = {uf: state for state, uf in DICT_STATES.items()}

class State:
    """
        Value Object para representar um estado brasileiro válido.

        Este Objeto encapsula a lógica de validação e formatação de um estado brasileiro.
        Ele é imutável após a criação, garantindo que o valor do estado não possa ser alterado.

        Características:
            - Validação de estado e UF
            - Fornece uma representação formatada para exibição
            - Pode ser utilizado em sets e como chave de dicionário
            - Garante imutabilidade após a criação
    """

    __slots__ = ("_state",)

    def __init__(self, state: str):
        state = self._normalize_string(state)
        self._validate_state(state)

        if state in DICT_UF:
            state = DICT_UF[state]

        object.__setattr__(self, "_state", state)

    @property
    def state(self) -> str:
        return self._state

    @property
    def uf(self) -> str:
        return DICT_STATES[self._state]
    
    @property
    def formatted(self) -> str:
        return f"{self._state} ({self.uf})"


    #---------------------------------------------------------------
    # Validação: método público para verificar se um estado é válido
    #---------------------------------------------------------------
   
    @classmethod
    def is_valid(cls, value: str) -> bool:
        try:
            cls(value)
            return True
        except StateError:
            return False


    #----------------------------------------------------
    # Normalização e Validação: método privado para padronizar e validar o estado
    #----------------------------------------------------

    @staticmethod
    def _normalize_string(value: str) -> str:
        if not isinstance(value, str):
            raise StateInvalidTypeError(type(value))
        
        value = value.strip()

        if len(value) == 2:
            return value.upper()

        return value.title()
    
    @staticmethod
    def _validate_state(value: str) -> None:
        if value not in DICT_STATES and value not in DICT_UF:
            raise StateInvalidError(value)

    
    #----------------------------------------------------
    # Igualdade: compara o valor do estado para igualdade
    #----------------------------------------------------

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, State):
            return NotImplemented
        return self._state == other._state


    #----------------------------------------------------
    # Hash: permite uso em sets e como chave de dicionário
    #----------------------------------------------------

    def __hash__(self) -> int:
        return hash(self._state)


    #----------------------------------------------------
    # Representação: string simples para exibição
    #----------------------------------------------------

    def __str__(self) -> str:
        return self.formatted


    #----------------------------------------------------
    # Representação: string formatada para exibição
    #----------------------------------------------------

    def __repr__(self) -> str:
        return f"State('{self.uf}')"
    

    #----------------------------------------------------
    # Imutabilidade: impede alterações após criação
    #----------------------------------------------------

    def __setattr__(self, key: str, value: object) -> None:
        raise StateError("State é imutável e não pode ser alterado após criação.")
