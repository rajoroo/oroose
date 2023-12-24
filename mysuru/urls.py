from django.urls import path

from . import views

urlpatterns = [
    path("stoch_daily/", views.stoch_daily_page, name="stoch_daily"),
    path("stoch_daily/load_top_ten/", views.load_stoch_daily_page, name="load_stoch_daily_page"),
    path("stoch_daily/calculate_top_ten/", views.calculate_stoch_daily_page, name="calculate_stoch_daily_page"),
    path("stoch_weekly/", views.stoch_weekly_page, name="stoch_weekly"),
    path("stoch_weekly/load_top_ten/", views.load_stoch_weekly_page, name="load_stoch_weekly_page"),
    path("stoch_weekly/calculate_top_ten/", views.calculate_stoch_weekly_page, name="calculate_stoch_weekly_page"),
    path("potential_stock/", views.potential_stock_page, name="potential_stock"),
    path("short_term/", views.short_term_page, name="short_term"),
]
