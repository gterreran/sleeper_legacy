from django.urls import path
# from . import views

# urlpatterns = [
#     path("login", views.login, name="login"),
# ]

from django.contrib.auth.views import LoginView

from .forms import UserLoginForm
from . import views

urlpatterns = [

    path(
        'login/',
        LoginView.as_view(
            template_name="account/login.html",
            authentication_form=UserLoginForm
            ),
        name='login'
    ),
    path("signup/", views.usersignup, name="signup"),
]