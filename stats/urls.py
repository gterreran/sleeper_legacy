from django.urls import path
from . import views
from django.shortcuts import redirect

# This needs to be imported here even if it's not used
from stats.dash_apps.finished_apps import fantasy_table

urlpatterns = [
    path('', lambda request: redirect('home')), 
    path("home/", views.home, name="home"),
    path("league/<league>", views.tables, name="tables"),
    path("profile/", views.profile, name="profile"),
]
