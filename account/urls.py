from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from . import views

urlpatterns = [
    path("login/", views.userlogin, name="login"),
    path("logout/", views.userlogout, name="logout"),
    path("signup/", views.usersignup, name="signup"),
    path(
        route = "forgot_password/",
        view = PasswordResetView.as_view(
            template_name = 'account/forgotpassword.html',
            email_template_name = 'account/password_reset_email.html',
            # subject_template_name = 'account/password_reset_subject.txt',
        ),
        name='reset_password'
    ),
    path("forgot_password_sent/", PasswordResetDoneView.as_view(), name='password_reset_done'),
    path("reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("reset_password_success/", PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]