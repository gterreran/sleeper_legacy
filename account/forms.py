from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_sleeper_username(sleeper_username):
    import requests
    # Need to check if sleeper username exists.
    url = f"https://api.sleeper.app/v1/user/{sleeper_username}"
    user_dict = requests.get(url).json()
    if user_dict is None:
        raise ValidationError(
            _('Username not find in Sleeper.'),
            code='invalid_username'
        )
    
class UserSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username']
        validate_sleeper_username(username)
        return username

class ForgottenPasswordForm(forms.Form):
    email = forms.EmailField(required=True)

class PasswordReset(SetPasswordForm):
    pass


