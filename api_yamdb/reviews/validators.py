from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(self, value):
    if value > timezone.now().year:
        raise ValidationError(
            f'Год выпуска не может быть больше текущего!'
            'Введите корректный год.'
        )