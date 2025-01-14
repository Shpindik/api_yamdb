from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class BaseModelViewSet(viewsets.ModelViewSet):
    """
    Базовый ViewSet с общей функциональностью для Category и Genre
    """
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    pagination_class = PageNumberPagination

    def retrieve(self, request, *args, **kwargs):
        """Метод GET для конкретного объекта запрещен"""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        """Метод PUT запрещен"""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
