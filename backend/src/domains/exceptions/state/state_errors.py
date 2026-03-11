from ..domain_errors import DomainError

class StateError(DomainError):
    """Base class for errors related to State value object."""
    pass

class StateInvalidTypeError(StateError):
    """Raised when the provided state is not a string."""
    def __init__(self, received_type: str):
        super().__init__(f"Expected a string for state, got {received_type}")

class StateInvalidError(StateError):
    """Raised when the provided state or UF is not found in the valid list."""
    def __init__(self, value: str):
        super().__init__(f"State '{value}' is not valid.")