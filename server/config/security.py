"""
Password hashing utilities.

Uses the `bcrypt` library directly (rather than passlib's bcrypt wrapper),
which avoids a known passlib/bcrypt version-detection incompatibility on
newer bcrypt releases. bcrypt truncates at 72 bytes internally, so long
passwords are pre-truncated explicitly to keep behaviour predictable.
"""
import bcrypt

_MAX_BCRYPT_BYTES = 72


def hash_password(plain_password: str) -> str:
    password_bytes = plain_password.encode("utf-8")[:_MAX_BCRYPT_BYTES]
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode("utf-8")[:_MAX_BCRYPT_BYTES]
    try:
        return bcrypt.checkpw(password_bytes, hashed_password.encode("utf-8"))
    except ValueError:
        return False
