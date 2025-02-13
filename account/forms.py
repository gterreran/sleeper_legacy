from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
    
class UserSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     validate_sleeper_username(username)
    #     return username

    def clean_email(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise ValidationError(
                _('Email already associated with an existing account.'),
                code='invalid_email'
            )
       return email

class ForgottenPasswordForm(forms.Form):
    email = forms.EmailField(required=True)

class PasswordReset(SetPasswordForm):
    pass


