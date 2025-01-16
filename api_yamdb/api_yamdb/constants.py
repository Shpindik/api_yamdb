MAX_EMAIL_LENGTH = 254
MAX_USERNAME_LENGTH = 150
MAX_LENGTH_NAME = 256
MAX_LENGTH_SLUG = 50
SHORT_TEXT_LENGTH = 25
MIN_SCORE_VALUE = 1
MAX_SCORE_VALUE = 10

EMPTY_VALUE = '-пусто-'
ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

CHOICES = (
    (ADMIN, 'Администратор'),
    (MODERATOR, 'Модератор'),
    (USER, 'Пользователь'),
)

BAD_USERNAME = [
    'me',
    'Me',
    'ME',
    ADMIN,
    MODERATOR,
    USER
]
