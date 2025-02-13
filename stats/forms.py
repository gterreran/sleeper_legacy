from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class NewSleeperUserForm(forms.Form):
    sleeper_username = forms.CharField(required=False)
    sleeper_userid = forms.CharField(required=False)


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
        import requests
        url = f"https://api.sleeper.app/v1/user/{field_value}"
        self.cleaned_data['user_dict'] = requests.get(url).json()
        if self.cleaned_data['user_dict'] is None:
            error = ValidationError(
                _(f"{field_type} not found in Sleeper."),
                code=f"invalid_{field_type}"
            )
            self.add_error(field_label, error)
        
        # If I got here, the query was successful.
        # For convenience, I append the `user_dict` to the cleaned_data
        # so that I won't have to query the sleeper server again.
        # self.cleaned_data['user_dict']=user_dict
        
