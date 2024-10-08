from django.urls import path

from . import views

urlpatterns = [
    # Trading
    path("trading_negative_page/", views.trading_negative_page, name="trading"),
    # Configuration
    path("trend/load_live", views.trend_page_load_live, name="trend_page_load_live"),
    path("trend/load_bhav", views.trend_page_load_bhav, name="trend_page_load_bhav"),
    path("trend/load_m15_short", views.trend_page_load_m15_short, name="trend_page_load_m15_short"),
    path("trend/futures", views.trend_page_load_futures, name="trend_page_load_futures"),
    path("trend/upload", views.trend_page_upload, name="trend_page_upload"),
    path("trend/<str:name>/fetch", views.trend_page_fetch, name="trend_page_fetch"),
    path("potential_trend/<str:name>/fetch", views.potential_trend_page_fetch, name="potential_trend_page_fetch"),
    path("trading/<str:name>/fetch", views.trading_page_fetch, name="trading_page_fetch"),
    path("trend/<str:name>/reset_fetch", views.trend_page_reset_fetch, name="trend_page_reset_fetch"),
    path("schedule_trading_start/", views.schedule_trading_start, name="schedule_trading_start"),
]
