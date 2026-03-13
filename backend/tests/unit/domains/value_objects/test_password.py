from domains.value_objects.password import Password
from hypothesis import given, strategies as st
from domains.exceptions import (
    PasswordError,
    PasswordInvalidTypeError,
    PasswordTooShortError,
    PasswordMissingUppercaseError,
    PasswordMissingLowercaseError,
    PasswordMissingNumberError,
    PasswordMissingSymbolError,
)
import pytest
import bcrypt
import random


PASSWORD_VALID = "Abcdef1!"
PASSWORD_TOO_SHORT = "Ab1!"
PASSWORD_NO_UPPER = "abcdef1!"
PASSWORD_NO_LOWER = "ABCDEF1!"
PASSWORD_NO_NUMBER = "Abcdefg!"
PASSWORD_NO_SYMBOL = "Abcdef12"


# ----------------------------------------
# Testes de criação e validação de Password
# ----------------------------------------

def test_create_valid_password():
    password = Password(PASSWORD_VALID)

    assert password.verify(PASSWORD_VALID) is True
    assert isinstance(password.hashed_password, str)


# ----------------------------------------
# Testes de exceções
# ----------------------------------------

@pytest.mark.parametrize(
    "plain_password,exception",
    [
        (123, PasswordInvalidTypeError),
        (PASSWORD_TOO_SHORT, PasswordTooShortError),
        (PASSWORD_NO_UPPER, PasswordMissingUppercaseError),
        (PASSWORD_NO_LOWER, PasswordMissingLowercaseError),
        (PASSWORD_NO_NUMBER, PasswordMissingNumberError),
        (PASSWORD_NO_SYMBOL, PasswordMissingSymbolError),
    ],
)
def test_invalid_password_raises_exception(plain_password, exception):
    with pytest.raises(exception):
        Password(plain_password)


# ----------------------------------------
# Testes de verificação de senha
# ----------------------------------------

def test_password_verify_correct_password():
    password = Password(PASSWORD_VALID)

    assert password.verify(PASSWORD_VALID) is True


def test_password_verify_wrong_password():
    password = Password(PASSWORD_VALID)

    assert password.verify("WrongPassword1!") is False


# ----------------------------------------
# Testes de propriedades
# ----------------------------------------

def test_password_properties():
    password = Password(PASSWORD_VALID)

    hashed = password.hashed_password

    assert isinstance(hashed, str)
    assert hashed != PASSWORD_VALID
    assert len(hashed) > 20


# ----------------------------------------
# Teste de fábrica from_hash
# ----------------------------------------

def test_password_factory_from_hash():
    hashed = bcrypt.hashpw(PASSWORD_VALID.encode(), bcrypt.gensalt())

    password = Password.from_hash(hashed.decode())

    assert password.hashed_password == hashed.decode()
    assert password.verify(PASSWORD_VALID) is True


# ----------------------------------------
# Teste de hash aleatório
# ----------------------------------------

def test_password_hash_is_random():
    p1 = Password(PASSWORD_VALID)
    p2 = Password(PASSWORD_VALID)

    assert p1.hashed_password != p2.hashed_password


# ----------------------------------------
# Teste de imutabilidade
# ----------------------------------------

def test_password_is_immutable():
    password = Password(PASSWORD_VALID)

    with pytest.raises(PasswordError):
        password.hashed_password = "new_hash"

    with pytest.raises(PasswordError):
        password._hashed_password = "new_hash"


# ----------------------------------------
# Teste de __repr__
# ----------------------------------------

def test_password_repr_does_not_expose_value():
    password = Password(PASSWORD_VALID)

    representation = repr(password)

    assert "<Password:" in representation
    assert PASSWORD_VALID not in representation


# ----------------------------------------
# Testes property-based com Hypothesis
# ----------------------------------------

@given(
    upper=st.sampled_from("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    lower=st.sampled_from("abcdefghijklmnopqrstuvwxyz"),
    digit=st.sampled_from("0123456789"),
    symbol=st.sampled_from("!@#$%^&*()"),
    rest=st.text(
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()",
        min_size=4,
        max_size=20
    ),
)
def test_password_with_random_valid_passwords(upper, lower, digit, symbol, rest):
    chars = list(upper + lower + digit + symbol + rest)

    random.shuffle(chars)

    plain_password = "".join(chars)

    password = Password(plain_password)

    assert password.verify(plain_password) is True