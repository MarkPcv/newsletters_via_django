from django.contrib.auth.views import LoginView as BaseLoginView

class LoginView(BaseLoginView):
    template_name = 'users/login.html'
