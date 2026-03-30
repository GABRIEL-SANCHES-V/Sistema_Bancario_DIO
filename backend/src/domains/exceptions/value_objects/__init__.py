#---------------------------------------------------------------
# Exceções relacionadas a Address
#---------------------------------------------------------------
from domains.exceptions.value_objects.address.address_errors import *


#---------------------------------------------------------------
# Exceções relacionadas a BirthDate
#---------------------------------------------------------------
from domains.exceptions.value_objects.birth_date import *


#---------------------------------------------------------------
# Exceções relacionadas a CPF
#---------------------------------------------------------------
from domains.exceptions.value_objects.cpf import *


#---------------------------------------------------------------
# Exceções relacionadas a ID de entidades
#---------------------------------------------------------------
from domains.exceptions.value_objects.id_entities import *


#---------------------------------------------------------------
# Exceções relacionadas a Email
#---------------------------------------------------------------
from domains.exceptions.value_objects.email import *


#---------------------------------------------------------------
# Exceções relacionadas a Money
#---------------------------------------------------------------
from domains.exceptions.value_objects.money import *


#---------------------------------------------------------------
# Exceções relacionadas a Name
#---------------------------------------------------------------
from domains.exceptions.value_objects.name import *


#---------------------------------------------------------------
# Exceções relacionadas a Password
#---------------------------------------------------------------
from domains.exceptions.value_objects.password import *


#---------------------------------------------------------------
# Exceções relacionadas a PhoneNumber
#---------------------------------------------------------------
from domains.exceptions.value_objects.phone_number import *


#---------------------------------------------------------------
# Exceções relacionadas a State
#---------------------------------------------------------------
from domains.exceptions.value_objects.state import *


#---------------------------------------------------------------
# Exceções relacionadas a ZipCode
#---------------------------------------------------------------
from domains.exceptions.value_objects.zip_code import *


__all__ = [
    "AddressError",
    "AddressInvalidTypeStateError",
    "AddressInvalidTypeZipCodeError",
    "AddressInvalidTypeError",
    "AddressInvalidValueError",

    "BirthDateError",
    "BirthDateInFutureError",
    "BirthDateTooOldError",
    "BirthDateInvalidTypeError",
    "BirthDateInvalidFormatError",
    "BirthDateInvalidValueError",

    "CPFError",
    "CPFInvalidLengthError",
    "CPFInvalidCheckDigitsError",
    "CPFRepeatedDigitsError",
    "CPFInvalidTypeError",

    "ClientIdError",
    "ClientIdInvalidTypeError",

    "AccountIdError",
    "AccountIdInvalidTypeError",

    "TransactionIdError",
    "TransactionIdInvalidTypeError",

    "EmailError",
    "EmailInvalidTypeError",

    "MoneyError",
    "MoneyInvalidTypeError",
    "MoneyInvalidValueError",

    "NameErrorVO",
    "NameInvalidTypeError",
    "NameTooShortError",
    "NameTooLongError",
    "NameInvalidFormatError",

    "PasswordError",
    "PasswordInvalidTypeError",
    "PasswordTooShortError",
    "PasswordMissingUppercaseError",
    "PasswordMissingLowercaseError",
    "PasswordMissingNumberError",
    "PasswordMissingSymbolError",

    "PhoneNumberError",
    "PhoneNumberInvalidLengthError",
    "PhoneNumberInvalidTypeError",
    "PhoneNumberMissingDigitError",
    "PhoneNumberInvalidDDDError",

    "StateError",
    "StateInvalidTypeError",
    "StateInvalidError",

    "ZipCodeError",
    "ZipCodeInvalidTypeError",
    "ZipCodeInvalidFormatError",
]