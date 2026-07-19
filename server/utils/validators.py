"""Reusable input validators for phone numbers, coordinates, and file uploads."""
import re

PHONE_REGEX = re.compile(r"^\+?[1-9]\d{7,14}$")


def is_valid_phone(phone: str) -> bool:
    return bool(PHONE_REGEX.match(phone))


def is_valid_coordinates(lat: float, lng: float) -> bool:
    return -90 <= lat <= 90 and -180 <= lng <= 180


def is_strong_password(password: str) -> bool:
    """At least 8 chars, one upper, one lower, one digit."""
    if len(password) < 8:
        return False
    return bool(re.search(r"[A-Z]", password) and re.search(r"[a-z]", password) and re.search(r"\d", password))
