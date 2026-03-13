#---------------------------------------------------------------
# Exceções relacionadas a Domain
#---------------------------------------------------------------
from .domain_errors import DomainError


#---------------------------------------------------------------
# Exceções relacionadas a Value Objects
#---------------------------------------------------------------
from domains.exceptions.value_objects import *


#---------------------------------------------------------------
# Exportação de todas as exceções
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
    
    "PasswordError",
    "PasswordInvalidTypeError",
    "PasswordTooShortError",
    "PasswordMissingUppercaseError",
    "PasswordMissingLowercaseError",
    "PasswordMissingNumberError",
    "PasswordMissingSymbolError",

    "EmailError",
    "EmailInvalidTypeError",

    "StateError",
    "StateInvalidTypeError",
    "StateInvalidError",

    "ZipCodeError",
    "ZipCodeInvalidTypeError",
    "ZipCodeInvalidFormatError",

    "AddressError",
    "AddressInvalidTypeStateError",
    "AddressInvalidTypeZipCodeError",
    "AddressInvalidTypeError",
    "AddressInvalidValueError",

    "NameErrorVO",
    "NameInvalidTypeError",
    "NameTooShortError",
    "NameTooLongError",
    "NameInvalidFormatError",
    
    "MoneyError",
    "MoneyInvalidTypeError",
    "MoneyInvalidValueError",
]