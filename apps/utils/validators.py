import re

from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r'^998[0-9]{9}$',
    message="Phone number must be entered in the format: '998 [XX] [XXX XX XX]'. Up to 12 digits allowed."
)


def is_phone_number(phone: str):
    pattern = r'^998[0-9]{9}$'
    match = re.match(pattern, phone)
    if match:
        return True
    else:
        return False
