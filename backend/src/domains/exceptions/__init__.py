#---------------------------------------------------------------
# Exceções relacionadas a Domain
#---------------------------------------------------------------
from .domain_errors import DomainError


#---------------------------------------------------------------
# Exceções relacionadas a CPF
#---------------------------------------------------------------
from .cpf import *


#---------------------------------------------------------------
# Exceções relacionadas a PhoneNumber
#---------------------------------------------------------------
from .phone_number import *


#---------------------------------------------------------------
# Exceções relacionadas a BirthDate
#---------------------------------------------------------------
from .birth_date import *

#---------------------------------------------------------------
# Exportação de todas as exceções para facilitar importação em outros módulos
#---------------------------------------------------------------
__all__ = [
    "DomainError",
    
    "CPFError",
    "CPFInvalidLengthError",
    "CPFInvalidCheckDigitsError",
    "CPFRepeatedDigitsError",
    "CPFInvalidTypeError",

    "PhoneNumberError",
    "PhoneNumberInvalidLengthError",
    "PhoneNumberInvalidTypeError",
    "PhoneNumberMissingDigitError",
    "PhoneNumberInvalidDDDError",

    "BirthDateError",
    "BirthDateInFutureError",
    "BirthDateTooOldError",
    "BirthDateInvalidTypeError",
    "BirthDateInvalidFormatError",
    "BirthDateInvalidValueError",
]