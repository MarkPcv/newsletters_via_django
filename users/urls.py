from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
#     path('logout/', LogoutView.as_view(), name='logout'),
#     path('register/', RegisterView.as_view(), name='register'),
#     path('resetpwd/', reset, name='reset'),
#     path('profile/', UserUpdateView.as_view(), name='profile'),
]