from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserProfile, League, Season, SleeperUser, SleeperPresident, Matchup

# Define an inline admin descriptor for the UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Legacy Sleeper User Profile"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(UserProfile)
admin.site.register(League)
admin.site.register(Season)
admin.site.register(SleeperUser)
admin.site.register(SleeperPresident)
admin.site.register(Matchup)
