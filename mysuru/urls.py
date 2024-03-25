from django.urls import path

from . import views

urlpatterns = [
    # Trend
    path("trend/<str:name>", views.trend_page, name="trend_page"),
    path("trend/<str:name>/load_live", views.trend_page_load_live, name="trend_page_load_live"),
    path("trend/<str:name>/load_bhav", views.trend_page_load_bhav, name="trend_page_load_bhav"),
    path("trend/<str:name>/upload", views.trend_page_upload, name="trend_page_upload"),
    path("trend/<str:name>/fetch", views.trend_page_fetch, name="trend_page_fetch"),
    path("trend/<str:name>/reset", views.trend_page_reset, name="trend_page_reset"),
    path("potential", views.potential_page, name="potential_page"),
    path("short_term", views.short_term_page, name="short_term_page"),
]
