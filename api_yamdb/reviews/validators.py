from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            'Год выпуска не может быть больше текущего!'
            'Введите корректный год.'
        )
