from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api_yamdb.constants import (
    BAD_USERNAME,
    MAX_USERNAME_LENGTH,
    MAX_EMAIL_LENGTH
)
from users.models import User
from users.validators import validate_username


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
