from django.urls import path

from . import views

urlpatterns = [
    path("<league>", views.index, name="index"),
    path("<league>/<user>", views.personal_page, name="user"),
]