from django.urls import path

from . import views

urlpatterns = [
    path("", views.m15_positive, name="trading_monitor"),
    path("m15_positive", views.m15_positive, name="m15_positive"),
    path("m15_negative", views.m15_negative, name="m15_negative"),
    path("daily_potential", views.daily_potential, name="daily_potential"),
]
