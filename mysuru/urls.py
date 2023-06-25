from django.urls import path

from . import views

urlpatterns = [
    path("macd/", views.macd_page, name="macd"),
    path("macd/load_top_ten/", views.load_macd_page, name="load_macd_page"),
    path("macd/calculate_top_ten/", views.calculate_macd_page, name="calculate_macd_page"),
    path("stoch_daily/", views.stoch_daily_page, name="stoch_daily"),
    path("stoch_daily/load_top_ten/", views.load_stoch_daily_page, name="load_stoch_daily_page"),
    path("stoch_daily/calculate_top_ten/", views.calculate_stoch_daily_page, name="calculate_stoch_daily_page"),
    path("stoch_weekly/", views.stoch_weekly_page, name="stoch_weekly"),
    path("stoch_weekly/load_top_ten/", views.load_stoch_weekly_page, name="load_stoch_weekly_page"),
    path("stoch_weekly/calculate_top_ten/", views.calculate_stoch_weekly_page, name="calculate_stoch_weekly_page"),
]
