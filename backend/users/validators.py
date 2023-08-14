from django.core.exceptions import ValidationError


def validate_username(value):
    """Username должен быть строкой и не должен быть 'me'."""
    if not isinstance(value, str):
        raise ValidationError(
            'username должен иметь тип str'
        )
    if value.lower() == 'me':
        raise ValidationError(
            f'username не может быть "{value}"'
        )
    return value
