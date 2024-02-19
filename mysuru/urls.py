from django.urls import path

from . import views

urlpatterns = [
    # Hourly
    path("stoch_hourly/", views.stoch_hourly_page, name="stoch_hourly"),
    path("stoch_hourly/load_top_ten/", views.load_stoch_hourly_page, name="load_stoch_hourly_page"),
    path("stoch_hourly/load_bhav/", views.load_bhav_stoch_hourly_page, name="load_bhav_stoch_hourly_page"),
    path("upload_hourly_stock_file/", views.upload_hourly_stock_file, name="upload_hourly_stock_file"),
    path("stoch_hourly/calculate_top_ten/", views.calculate_stoch_hourly_page, name="calculate_stoch_hourly_page"),
    # Daily
    path("stoch_daily/", views.stoch_daily_page, name="stoch_daily"),
    path("stoch_daily/load_top_ten/", views.load_stoch_daily_page, name="load_stoch_daily_page"),
    path("stoch_daily/load_bhav/", views.load_bhav_stoch_daily_page, name="load_bhav_stoch_daily_page"),
    path("upload_daily_stock_file/", views.upload_daily_stock_file, name="upload_daily_stock_file"),
    path("stoch_daily/calculate_top_ten/", views.calculate_stoch_daily_page, name="calculate_stoch_daily_page"),
    # Weekly
    path("stoch_weekly/", views.stoch_weekly_page, name="stoch_weekly"),
    path("stoch_weekly/load_top_ten/", views.load_stoch_weekly_page, name="load_stoch_weekly_page"),
    path("upload_weekly_stock_file/", views.upload_weekly_stock_file, name="upload_weekly_stock_file"),
    path("stoch_weekly/load_bhav/", views.load_bhav_stoch_weekly_page, name="load_bhav_stoch_weekly_page"),
    path("stoch_weekly/calculate_top_ten/", views.calculate_stoch_weekly_page, name="calculate_stoch_weekly_page"),
    # Others
    path("potential_stock/", views.potential_stock_page, name="potential_stock"),
    path("short_term/", views.short_term_page, name="short_term"),
]
