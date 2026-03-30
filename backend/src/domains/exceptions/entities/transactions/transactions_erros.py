from domains.exceptions import DomainError

class TransactionError(DomainError):
    pass

class TransactionAttributeError(TransactionError):
    def __init__(self, received_key: str):
        self.received_key = received_key
        super().__init__(
            f"O atributo '{self.received_key}' é imutável e não pode ser alterado após a criação do objeto Transaction"
        )

class TransactionDepositError(TransactionError):
    def __init__(self):
        super().__init__(
            "Transações do tipo DEPOSIT precisam ter uma conta de destino (to_account) associada."
        )

class TransactionWithdrawalError(TransactionError):
    def __init__(self):
        super().__init__(
            "Transações do tipo WITHDRAWAL precisam ter uma conta de origem (from_account) associada."
        )

class TransactionTransferError(TransactionError):
    def __init__(self):
        super().__init__(
            "Transações do tipo TRANSFER precisam ter contas de origem (from_account) e destino (to_account) associadas."
        )

class TransactionStatusTransitionError(TransactionError):
    def __init__(self, current_status: str, attempted_status: str):
        self.current_status = current_status
        self.attempted_status = attempted_status
        super().__init__(
            f"Transição de status inválida: não é possível mudar de '{self.current_status}' para '{self.attempted_status}'."
        )