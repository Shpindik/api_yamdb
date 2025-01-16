from django.db import models

from api_yamdb.constants import MAX_LENGTH_NAME, MAX_LENGTH_SLUG


class BaseModel(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Название',
        unique=True
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_SLUG,
        verbose_name='Идентификатор'
    )

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name
