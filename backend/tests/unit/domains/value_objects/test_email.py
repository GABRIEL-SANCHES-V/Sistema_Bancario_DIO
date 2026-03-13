from email_validator import EmailNotValidError
from hypothesis import given, strategies as st
from domains.value_objects.email import Email
from domains.exceptions import (
    EmailError,
    EmailInvalidTypeError,
)
import pytest


VALID_EMAIL = "Test@gmail.com"
VALID_EMAIL_NORMALIZED = "test@gmail.com"
VALID_EMAIL_MASKED = "t***t@gmail.com"

VALID_EMAIL_2 = "Another@outlook.com"
VALID_EMAIL_NORMALIZED_2 = "another@outlook.com"
VALID_EMAIL_MASKED_2 = "a***r@outlook.com"

VALID_EMAIL_3 = "TS@gmail.com"
VALID_EMAIL_NORMALIZED_3 = "ts@gmail.com"
VALID_EMAIL_MASKED_3 = "t***@gmail.com"


# ----------------------------------------
# Testes de criação e validação de Email
# ----------------------------------------

def test_create_valid_email():
    email = Email(VALID_EMAIL)

    assert email.value == VALID_EMAIL_NORMALIZED
    assert email.masked == VALID_EMAIL_MASKED


def test_create_email_with_normalized_value():
    email = Email(VALID_EMAIL_NORMALIZED)

    assert email.value == VALID_EMAIL_NORMALIZED


def test_create_email_with_invalid_type():
    with pytest.raises(EmailInvalidTypeError):
        Email(123)


# ----------------------------------------
# Testes de validação de Email
# ----------------------------------------

@pytest.mark.parametrize(
    "value,expected",
    [
        ("Test@gmail.com", True),
        ("test@gmail.com", True),
        ("another@test.com", True),
        ("TS@gmail.com", True),
        ("plainaddress", False),
        ("@missinglocal.com", False),
        ("missingatsign.com", False),
        ("missingdomain@.com", False),
        ("missingdot@com", False),
        ("two..dots@com", False),
        ("invalid@-domain.com", False),
        ("invalid@domain-.com", False),
        ("invalid@domain..com", False),
    ],
)
def test_email_is_valid(value, expected):
    assert Email.is_valid(value) is expected


# ----------------------------------------
# Testes de exceções
# ----------------------------------------

@pytest.mark.parametrize(
    "email",
    [
        "plainaddress",
        "@missinglocal.com",
        "missingatsign.com",
        "missingdomain@.com",
        "missingdot@com",
        "two..dots@com",
        "invalid@-domain.com",
        "invalid@domain-.com",
        "invalid@domain..com",
    ],
)
def test_invalid_email_raises_exception(email):
    with pytest.raises(EmailNotValidError):
        Email(email)


# ----------------------------------------
# Testes de propriedades
# ----------------------------------------

def test_email_properties():
    email1 = Email(VALID_EMAIL)
    email2 = Email(VALID_EMAIL_2)
    email3 = Email(VALID_EMAIL_3)

    assert email1.value == VALID_EMAIL_NORMALIZED
    assert email1.masked == VALID_EMAIL_MASKED

    assert email2.value == VALID_EMAIL_NORMALIZED_2
    assert email2.masked == VALID_EMAIL_MASKED_2

    assert email3.value == VALID_EMAIL_NORMALIZED_3
    assert email3.masked == VALID_EMAIL_MASKED_3


# ----------------------------------------
# Testes de igualdade
# ----------------------------------------

def test_email_equality():
    email1 = Email(VALID_EMAIL)
    email2 = Email(VALID_EMAIL_NORMALIZED)

    assert email1 == email2


def test_email_inequality():
    email1 = Email(VALID_EMAIL)
    email2 = Email(VALID_EMAIL_2)

    assert email1 != email2


# ----------------------------------------
# Teste de hash
# ----------------------------------------

def test_email_hash():
    email1 = Email(VALID_EMAIL)
    email2 = Email(VALID_EMAIL_NORMALIZED)

    assert hash(email1) == hash(email2)


def test_email_set_behavior():
    email1 = Email(VALID_EMAIL)
    email2 = Email(VALID_EMAIL_NORMALIZED)

    s = {email1, email2}

    assert len(s) == 1


# ----------------------------------------
# Teste de imutabilidade
# ----------------------------------------

def test_email_is_immutable():
    email = Email(VALID_EMAIL)

    with pytest.raises(EmailError):
        email.value = "new@email.com"


# ----------------------------------------
# Teste de __str__
# ----------------------------------------

def test_str_returns_email():
    email = Email(VALID_EMAIL)

    assert str(email) == VALID_EMAIL_NORMALIZED


# ----------------------------------------
# Teste de __repr__
# ----------------------------------------

def test_repr_contains_class_name():
    email = Email(VALID_EMAIL)

    representation = repr(email)

    assert "Email(" in representation
    assert VALID_EMAIL_NORMALIZED in representation


# ----------------------------------------
# Testes property-based com Hypothesis
# ----------------------------------------

@given(st.emails())
def test_email_normalization_with_random_emails(email):
    obj = Email(email)

    assert obj.value == obj.value.lower()
    assert "@" in obj.value