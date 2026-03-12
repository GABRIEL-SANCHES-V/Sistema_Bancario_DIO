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
# Exceções relacionadas a Password
#---------------------------------------------------------------
from .password import *


#---------------------------------------------------------------
# Exceções relacionadas a Email
#---------------------------------------------------------------
from .email import *


#---------------------------------------------------------------
# Exceções relacionadas a State
#---------------------------------------------------------------
from .state import *


#---------------------------------------------------------------
# Exceções relacionadas a ZipCode
#---------------------------------------------------------------
from .zip_code.zip_code_errors import *


#---------------------------------------------------------------
# Exceções relacionadas a Address
#---------------------------------------------------------------
from .address.address_errors import *


#---------------------------------------------------------------
# Exceções relacionadas a Name
#---------------------------------------------------------------
from .name import *


#---------------------------------------------------------------
# Exceções relacionadas a Money
#---------------------------------------------------------------
from .money import *


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