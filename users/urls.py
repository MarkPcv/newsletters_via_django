from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, ProfileView, \
    activate_user

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('activate/<user_pk>', activate_user, name='activate_user'),
]