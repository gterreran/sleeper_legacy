from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import requests

from stats.models import UserProfile, SleeperUser, League, Season

class NewSleeperUserForm(forms.Form):
    sleeper_username = forms.CharField(required=False)
    sleeper_userid = forms.CharField(required=False)

    # Grabbing the user to be used for my validation
    def __init__(self, *args, user=None, **kwargs):
            super().__init__(*args, **kwargs)
            self.user = user

    def clean(self):
        cleaned_data = super().clean()
        sleeper_username = cleaned_data.get("sleeper_username")
        sleeper_userid = cleaned_data.get("sleeper_userid")

        # If the Username is provided, I'll validate the existence of
        # the user in Sleeper with it, otherwise I'll do it with
        # the User ID. If neither are provided, I'm raising an error.
        # The existence of the user will be checked cleaning the proxy
        # field `field_value`.
        if sleeper_username:
            field_label = 'sleeper_username'
            field_value = sleeper_username
            field_type = 'Username'
        elif sleeper_userid:
            field_label = 'sleeper_userid'
            field_value = sleeper_userid
            field_type = 'UserID'

        if not sleeper_username and not sleeper_userid:
            raise ValidationError(
                _('You need to specify at least one of the two fields.'),
                code="missing_field"
            )
        
        # If I got here, it means that I have either of the 2 values
        
        # When I add a new SleeperUser, I will automatically add also
        # all the SleeperUsers that are in their leagues. So chances are
        # that when a new user add a new SleeperUser, that might be
        # in the database already.
        # I check if the SleeperUser exists here, even though I will not
        # throw an error if it does. I do it this way so I can avoid
        # to query the sleeper API twice.
        new_user = False
        try:
            sleeper_user = SleeperUser.objects.get(sleeper_userid=field_value)
        except SleeperUser.DoesNotExist:
            try:
                sleeper_user = SleeperUser.objects.get(sleeper_username=field_value)
            except SleeperUser.DoesNotExist:
                new_user = True
        
        # The cleaned_data['user_dict'] will different, depending if the
        # SleeperUser existed already in the database or not
        if new_user: 
            url = f"https://api.sleeper.app/v1/user/{field_value}"
            sleeper_json = requests.get(url).json()
            if self.cleaned_data['user_dict'] is None:
                error = ValidationError(
                    _(f"{field_type} not found in Sleeper."),
                    code=f"invalid_{field_type}"
                )
                self.add_error(field_label, error)
            self.cleaned_data['user_dict'] = {
                'new_user' : True,
                **sleeper_json
            }
        else:
            if sleeper_user in UserProfile.objects.get(user=self.user).sleeperusers.all():
                error = ValidationError(
                    _(f"{field_type} already present in your profile."),
                    code=f"existing_sleeper_user"
                )
            self.cleaned_data['user_dict'] = {
                'new_user' : False,
                'sleeper_user' : sleeper_user
            }

            
        
        # If I got here, the query was successful.
        # For convenience, I append the `user_dict` to the cleaned_data
        # so that I won't have to query the sleeper server again.
        # self.cleaned_data['user_dict']=user_dict
        
