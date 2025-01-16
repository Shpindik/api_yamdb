import django_filters

from reviews.models import Title


class FilterTitle(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name='category__slug',
        lookup_expr='iexact'
    )
    genre = django_filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='iexact'
    )
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    year = django_filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ('year', 'category', 'genre', 'name')
