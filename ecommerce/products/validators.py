from django.core.exceptions import ValidationError  

def price_validator(value):
    if value < 0:
        raise ValidationError("Price cannot be negative.")
    if value > 100000:
        raise ValidationError("Price cannot exceed 100,000.")