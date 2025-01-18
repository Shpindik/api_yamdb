from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
)
from rest_framework.response import Response

from api.permissions import IsAdmin
from api.serializers import (
    UserAccessTokenSerializer,
    UserCreationSerializer,
    UserSerializer
)
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .filters import FilterTitle
from .permissions import IsAdminModeratorAuthorOrReadOnly, IsAdminOrReadOnly
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer
)
from .viewset import ListCreateDeleteViewSet


class CategoryViewSet(ListCreateDeleteViewSet):
    """Работа с категориями."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDeleteViewSet):
    """Работа с жанрами."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Работа с произведениями."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    serializer_class = TitleReadSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterTitle
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete']
    ordering_fields = ['name', 'year', 'rating']
    ordering = ['name']

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Работа с отзывами на произведения."""

    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminModeratorAuthorOrReadOnly,
    ]

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Работа с комментариями."""

    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminModeratorAuthorOrReadOnly
    ]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_review().comments.select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup(request):
    serializer = UserCreationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    serializer = UserAccessTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data['username']
    )
    token = default_token_generator.make_token(user)
    return Response({'token': token}, status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Представление пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ['username']
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(self.request.user)
            return Response(serializer.data, status.HTTP_200_OK)
        serializer = UserSerializer(
            self.request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data, status.HTTP_200_OK)
