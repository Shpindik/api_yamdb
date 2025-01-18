from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api_yamdb.constants import (
    BAD_USERNAME,
    MAX_EMAIL_LENGTH,
    MAX_SCORE_VALUE,
    MAX_USERNAME_LENGTH,
    MIN_SCORE_VALUE
)
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from users.validators import validate_username


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category

    def validate_slug(self, value):
        if Category.objects.filter(slug=value).exists():
            raise serializers.ValidationError(
                'Категория с таким slug уже существует.'
            )
        return value


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')

    def validate_slug(self, value):
        if Genre.objects.filter(slug=value).exists():
            raise serializers.ValidationError(
                'Жанр с таким slug уже существует.'
            )
        return value


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        allow_empty=False
    )

    class Meta:
        model = Title
        fields = '__all__'

    def to_representation(self, instance):
        return TitleReadSerializer(instance).data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    score = serializers.IntegerField(
        min_value=MIN_SCORE_VALUE,
        max_value=MAX_SCORE_VALUE,
        error_messages={
            'min_value': f'Оценка не может быть меньше {MIN_SCORE_VALUE}.',
            'max_value': f'Оценка не может быть больше {MAX_SCORE_VALUE}.'
        }
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        if request.method == 'POST' and Review.objects.filter(
            title_id=title_id,
            author=author
        ).exists():
            raise ValidationError('Отзыв уже оставлен.')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class UserCreationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=MAX_EMAIL_LENGTH)
    username = serializers.CharField(
        max_length=MAX_USERNAME_LENGTH,
        validators=[UnicodeUsernameValidator(), validate_username])

    def validate(self, data):
        if data['username'] in BAD_USERNAME:
            raise serializers.ValidationError(
                'Нельзя создать пользователя с username={}.', data['username']
            )
        user_email = User.objects.filter(email=data['email']).first()
        user_username = User.objects.filter(username=data['username']).first()
        if user_email != user_username:
            msg = 'email' if user_email else 'username'
            raise serializers.ValidationError(
                'Пользователь с таким {} уже существует.'.format(msg)
            )
        return data

    def create(self, validated_data):
        user, _ = User.objects.get_or_create(
            email=validated_data['email'],
            username=validated_data['username']
        )
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.save()
        send_mail(
            subject='Код подтверждения Yamdb',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[validated_data['email']],
        )
        return user


class UserAccessTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        confirmation_code = data['confirmation_code']
        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения'}
            )
        return data
