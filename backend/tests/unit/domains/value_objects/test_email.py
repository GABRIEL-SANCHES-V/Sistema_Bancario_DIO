from email_validator import EmailNotValidError
from hypothesis import given, strategies as st
from domains.value_objects.email import Email
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


# -----------------------------
# Creation tests
# -----------------------------

def test_create_valid_email():
    email = Email(VALID_EMAIL)

    assert email.value == VALID_EMAIL_NORMALIZED
    assert email.masked == VALID_EMAIL_MASKED


def test_create_already_normalized_email():
    email = Email(VALID_EMAIL_NORMALIZED)

    assert email.value == VALID_EMAIL_NORMALIZED
    assert email.masked == VALID_EMAIL_MASKED


# -----------------------------
# Exception tests
# -----------------------------

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


# -----------------------------
# is_valid tests
# -----------------------------

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


# -----------------------------
# Equality tests
# -----------------------------

def test_email_equality():
    email1 = Email(VALID_EMAIL)
    email2 = Email(VALID_EMAIL_NORMALIZED)
    email3 = Email(VALID_EMAIL_2)

    assert email1 == email2
    assert email1 != email3


# -----------------------------
# Hash tests
# -----------------------------

def test_email_hash():
    email1 = Email(VALID_EMAIL)
    email2 = Email(VALID_EMAIL_NORMALIZED)
    email3 = Email(VALID_EMAIL_2)

    assert hash(email1) == hash(email2)
    assert hash(email1) != hash(email3)


# -----------------------------
# Immutability tests
# -----------------------------

def test_email_is_immutable():
    email = Email(VALID_EMAIL)

    with pytest.raises(AttributeError):
        email.value = "new@email.com"


# -----------------------------
# Mask tests
# -----------------------------

def test_email_masked():
    email1 = Email(VALID_EMAIL)
    email2 = Email(VALID_EMAIL_2)
    email3 = Email(VALID_EMAIL_3)

    assert email1.masked == VALID_EMAIL_MASKED
    assert email2.masked == VALID_EMAIL_MASKED_2
    assert email3.masked == VALID_EMAIL_MASKED_3


# -----------------------------
# Representation tests
# -----------------------------

def test_email_str():
    email = Email(VALID_EMAIL)

    assert str(email) == VALID_EMAIL_NORMALIZED


def test_email_repr():
    email = Email(VALID_EMAIL)

    assert repr(email) == "Email('test@gmail.com')"


# -----------------------------
# Property-based tests
# -----------------------------

@given(st.emails())
def test_random_valid_emails(email):
    obj = Email(email)

    assert obj.value == obj.value.lower()