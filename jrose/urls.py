from django.urls import path

from . import views

urlpatterns = [
    path("week_page", views.week_page, name="week_page"),
]
