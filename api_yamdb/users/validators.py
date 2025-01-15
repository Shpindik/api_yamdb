from django.core.exceptions import ValidationError

from api_yamdb.constants import BAD_USERNAME


def validate_username(value):
    if value in BAD_USERNAME:
        raise ValidationError(
            f'Нельзя создать пользователя с username={value}.'
        )
