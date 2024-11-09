from django.contrib import admin

from .models import League, Season, User, Username, Matchup

admin.site.register(League)
admin.site.register(Season)
admin.site.register(User)
admin.site.register(Username)
admin.site.register(Matchup)
