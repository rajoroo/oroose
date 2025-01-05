from django.urls import path

from . import views

urlpatterns = [
    path("week_page", views.week_page, name="week_page"),
    path("day_page", views.day_page, name="day_page"),
    path("smart_buy_page", views.smart_buy_page, name="smart_buy_page"),
    path("week_level_0_to_20_page", views.week_level_0_to_20_page, name="week_level_0_to_20_page"),
    path("week_level_20_to_50_page", views.week_level_20_to_50_page, name="week_level_20_to_50_page"),
    path("week_level_50_to_80_page", views.week_level_50_to_80_page, name="week_level_50_to_80_page"),
]
