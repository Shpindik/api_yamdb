from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from reviews.models import Category, Genre, Title
from .base import BaseModelViewSet
from .permissions import (
    IsAdminOrReadOnly,
    IsAdmin,
    IsAdminModeratorAuthorOrReadOnly
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleWriteSerializer
)
from .filters import TitleFilter


class CategoryViewSet(BaseModelViewSet):
    """ViewSet для работы с категориями"""
    queryset = Category.objects.all().select_related(
        'category'
    ).prefetch_related(
        'titles'
    )
    serializer_class = CategorySerializer


class GenreViewSet(BaseModelViewSet):
    """ViewSet для работы с жанрами"""
    queryset = Genre.objects.all().prefetch_related(
        'titles'
    )
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с произведениями"""
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """
        Возвращает оптимизированный queryset с аннотированным полем rating
        """
        return Title.objects.select_related(
            'category'
        ).prefetch_related(
            'genre',
            'reviews'
        ).annotate(
            rating=Avg('reviews__score')
        )

    def get_serializer_class(self):
        """
        Возвращает разные сериализаторы для чтения и записи
        """
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer
