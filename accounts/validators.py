from msilib.schema import _Validation_records
from xml.dom import ValidationErr
from django.utils.translation import gettext_lazy

from django.core.exceptions import ValidationError

import re

def email_validator(email):
    express = r"[-_.]*[a-zA-z0-9]+@[a-z]+(\.[a-z]+)"
    regex = re.compile(express)
    result = re.match(regex, email)
    if result is None:
        raise ValidationError('Invalid Email')

def username_validator(username):
    express = r"[@._]*[A-Za-z]+[0-9.@-_]*"
    regex = re.compile(express)
    result = re.match(regex, username)
    if result is None:
        raise ValidationError("Invalid Username")