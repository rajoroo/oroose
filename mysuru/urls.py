from django.urls import path

from . import views

urlpatterns = [
    # Trend
    path("trend/load_live", views.trend_page_load_live, name="trend_page_load_live"),
    path("trend/load_bhav", views.trend_page_load_bhav, name="trend_page_load_bhav"),
    path("trend/futures", views.trend_page_load_futures, name="trend_page_load_futures"),
    path("trend/upload", views.trend_page_upload, name="trend_page_upload"),
    path("trend/<str:name>/fetch", views.trend_page_fetch, name="trend_page_fetch"),
]
