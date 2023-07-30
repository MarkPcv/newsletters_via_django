from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, ProfileView, \
    activate_user, deactivate_newsletter, UserListView, deactivate_user

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('activate/<user_pk>', activate_user, name='activate_user'),
    path('deactivate/newsletter/<int:pk>', deactivate_newsletter, name='deactivate_newsletter'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('deactivate/user/<int:pk>', deactivate_user, name='deactivate_user'),
]