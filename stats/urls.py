from django.urls import path
from . import views
# from stats.dash_apps.finished_apps import fantasy_table

urlpatterns = [
    path("", views.home, name="home"),
    path("<league>", views.tables, name="tables"),
    path("<league>/<user>", views.personal_page, name="user"),
]
