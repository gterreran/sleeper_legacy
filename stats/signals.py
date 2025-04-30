from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserProfile, Season, League

# When a new User is created, a UserProfile instance is also created
@receiver(post_save, sender=get_user_model())
def create_userprofile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# When the Season name is updated, also the league nickname is.
# Unless the flag custom_name is True.
@receiver(post_save, sender=Season)
def update_league(sender, instance, created, **kwargs):
    if created:
        league = instance.league
        if instance.year > league.most_recent_year:
            league.most_recent_year = instance.year
            league.avatar = instance.avatar
            league.name = instance.name
            league.save()
