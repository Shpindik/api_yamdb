<div id="header" align="left">
    <img src="https://img.shields.io/badge/Python-blue?logo=python&logoColor=yellow" alt="Python"/>
    <img src="https://img.shields.io/badge/Django-dark_green?logo=django&logoColor=white" alt="Django"/>
    <img src="https://img.shields.io/badge/Django-rest-red?logo=django&logoColor=white" alt="Django Rest"/>
</div>

# Проект YaMDb

## Описание
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». 
Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 

## Технологии используемые в проекте:
- python==3.9.13
- requests==2.26.0
- Django==3.2
- djangorestframework==3.12.4
- PyJWT==2.1.0
- pytest==6.2.4
- pytest-django==4.4.0
- pytest-pythonpath==0.7.3
- djangorestframework-simplejwt==4.7.2
- django-filter==22.1
- setuptools==57.4.0


## Инструкция по запуску

1) Клонировать репозиторий и перейти в него в командной строке:

```
git clone --single-branch --branch master https://github.com/Shpindik/api_yamdb.git
```

```
cd api_yamdb
```

2) Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
source venv/Scripts/activate
```

3) Установить зависимости из файла requirements.txt:

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

4) Выполнить миграции:

```bash
python manage.py migrate
```

5) Создать суперпользователя:

```bash
python manage.py createsuperuser
```

6) Запустить проект:

```bash
python manage.py runserver
```


## Как наполнить БД
Запуск команды загрузки данных из CSV в БД.

```bash
python manage.py upload_data
```

Соответствике моделей с файлами:
- Пользователи <-- users.csv
- Жанры <-- genre.csv
- Категории <-- category.csv
- Произведения и жанры <-- genre_title.csv
- Произведения <-- titles.csv
- Отзывы <-- review.csv
- Комментарии <-- comments.csv

## Документация к API
После запуска проекта доступна документация по адресу: http://127.0.0.1:8000/redoc/

## Примеры запросов:
- Получение списка всех произведений
  > Request: 
  ```
  [GET] /api/v1/titles/
  ```
  > Response:
  ```json
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {
            "name": "string",
            "slug": "^-$"
          }
        ],
        "category": {
          "name": "string",
          "slug": "^-$"
        }
      }
    ]
  }
  ```
- Добавление произведения
  > Request: 
  ```
  [POST] /api/v1/posts/
  ```
  > Payload:
  ```json
  {
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
      "string"
    ],
    "category": "string"
  }
  ```
  > Response:
  ```json
  {
    "id": 0,
    "name": "string",
    "year": 0,
    "rating": 0,
    "description": "string",
    "genre": [
      {}
    ],
    "category": {
      "name": "string",
      "slug": "^-$"
    }
  }
  ```
- Получение списка всех отзывов
  > Request: 
  ```
  [GET] /api/v1/titles/{title_id}/reviews/
  ```
  > Response:
  ```json
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2024-12-08T20:15:22Z"
      }
    ]
  }
  ``` 
- Добавление нового отзыва
  > Request: 
  ```
  [POST] /api/v1/titles/{title_id}/reviews/
  ```
  > Payload:
  ```json
  {
    "text": "string",
    "score": 1
  }
  ```
  > Response:
  ```json
  {
    "id": 0,
    "text": "string",
    "author": "string",
    "score": 1,
    "pub_date": "2024-12-08T20:15:22Z"
  }
  ```
- Получение списка всех комментариев к отзыву
  > Request: 
  ```
  [GET] /api/v1/titles/{title_id}/reviews/{review_id}/comments/
  ```
  > Response:
  ```json
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
  ```
- Добавление комментария к отзыву
  > Request: 
  ```
  [POST] /api/v1/titles/{title_id}/reviews/{review_id}/comments/
  ```
  > Payload:
  ```json
  {
    "text": "string"
  }
  ```
  > Response:
  ```json
  {
    "id": 0,
    "text": "string",
    "author": "string",
    "pub_date": "2024-12-08T20:15:22Z"
  }
  ```

## Авторы
#### [GITHUB](https://github.com/Shpindik) Александр П.
#### [GITHUB](https://github.com/sergey-vg) Сергей В.
#### [GITHUB](https://github.com/DamirProject) Дамир Б.   
