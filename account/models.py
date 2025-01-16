from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class SLUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sleeper_username = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
    
