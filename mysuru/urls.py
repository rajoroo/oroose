from django.urls import path

from . import views

urlpatterns = [
    # Configuration
    path("trend/upload", views.trend_page_upload, name="trend_page_upload"),
    path("trend/<str:name>/fetch", views.trend_page_fetch, name="trend_page_fetch"),
    path("trend/<str:name>/reset_fetch", views.trend_page_reset_fetch, name="trend_page_reset_fetch"),
]
