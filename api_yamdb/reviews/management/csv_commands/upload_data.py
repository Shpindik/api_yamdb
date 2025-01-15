from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from reviews.management.csv_commands.upload import (
    upload_data,
    upload_data_title_genre
)
from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre


User = get_user_model()


FILE_MODEL = {
    'users.csv': User,
    'category.csv': Category,
    'genre.csv': Genre,
    'titles.csv': Title,
    'review.csv': Review,
    'comments.csv': Comment,
}


class Command(BaseCommand):
    help = 'Загружает данные из CSV файлов в базу данных'

    def handle(self, *args, **options):
        for file, model in FILE_MODEL.items():
            name = model.__name__
            self.stdout.write(f'Загрузка данных из {file} в модель {name}...')
            upload_data(file, model)
        self.stdout.write('Установка связей между произведениями и жанрами...')
        upload_data_title_genre(TitleGenre, 'genre_title.csv')
        self.stdout.write(self.style.SUCCESS('Данные успешно загружены!'))
