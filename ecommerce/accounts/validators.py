from django.core.validators import RegexValidator
import re 
from django.core.exceptions import ValidationError


def username_validator(value):
    """
    Validate that the username contains only alphanumeric characters and underscores.
    
    Args:
        value (str): The username to validate.
    
    Raises:
        ValidationError: If the username contains invalid characters.
    """
    pattern = r'^[a-zA-Z0-9_]+$'
    if not re.match(pattern, value):
        raise ValidationError("Usernames can only contain letters, numbers and underscores.")
    if not re.search(r'[a-zA-Z]', value):
        raise ValidationError("Username must contain at least one alphabet.")
    
def phone_number_validator(value):
    """
    Validate that the phone number is in a valid format.
    
    Args:
        value (str): The phone number to validate.
    
    Raises:
        ValidationError: If the phone number is not valid.
    """
    if not value.isdigit():
        raise ValidationError("Phone number must contain only digits.")
    if len(value) != 10:
        raise ValidationError("Please enter a valid 10-digit phone number.")


name_validator = RegexValidator(
    r"^[a-zA-Z\s]+$", "Enter a Valid name (Only alphabets and spaces)"
)
