from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from api_yamdb.constants import EMPTY_VALUE
from users.models import User


admin.site.empty_value_display = EMPTY_VALUE


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role']
    list_editable = ('role',)
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'username',
                    'first_name',
                    'last_name',
                    'role',
                    'email',
                    'bio',
                ),
            },
        ),
        (
            'Дополнительно',
            {
                'fields': (
                    'password',
                    'last_login',
                    'is_superuser',
                    'is_staff',
                    'is_active',
                    'date_joined',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
    )
