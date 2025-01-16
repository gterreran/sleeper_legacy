from django.contrib.auth.models import User
from .models import SLUser
from django.contrib.auth.backends import BaseBackend

class ExtendedAuthBackend(BaseBackend):
    """
    Authenticate using username, e-mail address or sleeper_id
    """
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                try:
                    user = SLUser.objects.get(sleeper_id=username).user
                except User.DoesNotExist:
                    return None

        if user.check_password(password):
            return user
        else:
            return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None