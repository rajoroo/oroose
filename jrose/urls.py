from django.urls import path

from . import views

urlpatterns = [
    path("week_page", views.week_page, name="week_page"),
    path("day_page", views.day_page, name="day_page"),
    path("smart_buy_page", views.smart_buy_page, name="smart_buy_page"),
]
