from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, get_token, signup

app_name = 'users'

v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')

auth_urls = [
    path('token/', get_token, name='token'),
    path('signup/', signup, name='signup'),
]

pattern_list = [
    path('auth/', include(auth_urls)),
    path('', include(v1_router.urls)),
]

urlpatterns = [
    path('v1/', include(pattern_list)),
]
