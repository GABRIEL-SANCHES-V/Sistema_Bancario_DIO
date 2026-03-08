from email_validator import validate_email, EmailNotValidError


class Email:
    """
        Value Object para representar um endereço de email válido.

        Este Objeto encapsula a lógica de validação e formatação de um email.
        Ele é imutável após a criação, garantindo que o valor do email não possa ser alterado.

        Características:
            - Valida o formato do email usando a biblioteca email_validator
            - Fornece uma representação mascarada do email para exibição segura
            - Pode ser utilizado em sets e como chave de dicionário
            - Garante imutabilidade após a criação
    """

    __slots__ = ("_value",)

    def __init__(self, value: str) -> None:

        if not isinstance(value, str):
            raise TypeError("Email deve ser fornecido como string")

        validated = validate_email(
            value,
            check_deliverability=False # Desabilita verificação de entregabilidade para evitar falhas em testes e ambientes sem acesso à internet
        )

        object.__setattr__(self, "_value", validated.normalized.lower())

    @property
    def value(self) -> str:
        return self._value

    @property
    def masked(self) -> str:
        local, domain = self._value.split("@")

        if len(local) <= 2:
            masked = local[0] + "***"
        else:
            masked = f"{local[0]}***{local[-1]}"

        return f"{masked}@{domain}"


    #---------------------------------------------------------------
    # Validação: método público para verificar se um email é válido
    #---------------------------------------------------------------
    @classmethod
    def is_valid(cls, value: str) -> bool:
        try:
            cls(value)
            return True
        except EmailNotValidError:
            return False

    
    #----------------------------------------------------
    # Igualdade: compara o valor do email para igualdade
    #----------------------------------------------------
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Email):
            return NotImplemented
        return self._value == other._value


    #----------------------------------------------------
    # Hash: permite uso em sets e como chave de dicionário
    #----------------------------------------------------
    def __hash__(self) -> int:
        return hash(self._value)


    #----------------------------------------------------
    # Representação: string simples para exibição
    #----------------------------------------------------
    def __str__(self) -> str:
        return self._value


    #----------------------------------------------------
    # Representação: string formatada para exibição
    #----------------------------------------------------
    def __repr__(self) -> str:
        return f"Email('{self._value}')"


    #----------------------------------------------------
    # Imutabilidade: impede alterações após criação
    #----------------------------------------------------
    def __setattr__(self, key, value):
        raise AttributeError("Email é um objeto imutável")