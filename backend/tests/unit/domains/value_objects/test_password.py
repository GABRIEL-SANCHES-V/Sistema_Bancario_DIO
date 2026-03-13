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


# -----------------------------
# Creation tests
# -----------------------------

def test_create_valid_password():
    password = Password(PASSWORD_VALID)
    assert password.verify(PASSWORD_VALID) is True




# ------------------------------
# Exception tests
# ------------------------------
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


# ------------------------------
# is_valid tests
# ------------------------------
def test_password_verify_wrong_password():
    password = Password(PASSWORD_VALID)

    assert password.verify("WrongPassword1!") is False

# ------------------------------
# Representation tests
# ------------------------------
def test_password_representation():
    password = Password(PASSWORD_VALID)
    repr_str = repr(password)

    assert repr_str == "<Password: *****>"
    assert PASSWORD_VALID not in repr_str


# ------------------------------
# Test Factory from_hash
# ------------------------------
def test_password_factory_from_hash():
    hashed = bcrypt.hashpw(PASSWORD_VALID.encode('utf-8'), bcrypt.gensalt())
    password = Password.from_hash(hashed.decode('utf-8'))

    assert password.hashed_password == hashed.decode('utf-8')
    assert password.verify(PASSWORD_VALID) is True


# ------------------------------
# Immutability tests
# ------------------------------
def test_password_immutable():
    password = Password(PASSWORD_VALID)

    with pytest.raises(PasswordError):
        password.hashed_password = "new_hash"

    with pytest.raises(PasswordError):
        password._hashed_password = "new_hash"


#------------------------------
# Hash randomness tests
#------------------------------
def test_password_hash_is_random():
    p1 = Password(PASSWORD_VALID)
    p2 = Password(PASSWORD_VALID)

    assert p1.hashed_password != p2.hashed_password

# ------------------------------
# Property-based tests
# ------------------------------
@given(
    upper=st.sampled_from("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    lower=st.sampled_from("abcdefghijklmnopqrstuvwxyz"),
    digit=st.sampled_from("0123456789"),
    symbol=st.sampled_from("!@#$%^&*()"),
    rest=st.text(
    alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()",
    min_size=4,
    max_size=20
)
)
def test_password_with_random_valid_passwords(upper, lower, digit, symbol, rest):
    chars = list(upper + lower + digit + symbol + rest)
    random.shuffle(chars)
    plain_password = "".join(chars)
    password = Password(plain_password)

    assert password.verify(plain_password)
