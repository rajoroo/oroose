from django.urls import path

from . import views

urlpatterns = [
    # Trend
    path("stock_data_week_page/", views.stock_data_week_page, name="stock_data"),
    path("stock_data_day_page/", views.stock_data_day_page, name="stock_data_day"),
    path("stock_data_hour_page/", views.stock_data_hour_page, name="stock_data_hour"),
    path("stock_data_15min_page/", views.stock_data_15min_page, name="stock_data_15min"),
    path("stock_data_5min_page/", views.stock_data_5min_page, name="stock_data_5min"),
    # Potential
    path("potential_page/", views.potential_page, name="potential"),
    # Short Term
    path("short_term_page/", views.short_term_page, name="short_term"),
    # Intraday
    path("intraday_m15_positive_page/", views.intraday_m15_positive_page, name="intraday"),
    path("intraday_m15_negative_page/", views.intraday_m15_negative_page, name="intraday_negative"),
    # Trading
    path("trading_negative_page/", views.trading_negative_page, name="trading"),
    # Configuration
    path("trend/load_live", views.trend_page_load_live, name="trend_page_load_live"),
    path("trend/load_bhav", views.trend_page_load_bhav, name="trend_page_load_bhav"),
    path("trend/futures", views.trend_page_load_futures, name="trend_page_load_futures"),
    path("trend/upload", views.trend_page_upload, name="trend_page_upload"),
    path("trend/<str:name>/fetch", views.trend_page_fetch, name="trend_page_fetch"),
    path("potential_trend/<str:name>/fetch", views.potential_trend_page_fetch, name="potential_trend_page_fetch"),
    path("trading/<str:name>/fetch", views.trading_page_fetch, name="trading_page_fetch"),
    path("trend/<str:name>/reset_fetch", views.trend_page_reset_fetch, name="trend_page_reset_fetch"),
    path("schedule_trading_start/", views.schedule_trading_start, name="schedule_trading_start"),
]
