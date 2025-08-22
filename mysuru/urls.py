from django.urls import path

from . import views

urlpatterns = [
    # Configuration
    path("stock_collection/upload", views.stock_collection_upload, name="stock_collection_upload"),
    path(
        "stock_collection/fetch_smart_token",
        views.stock_collection_fetch_smart_token,
        name="stock_collection_fetch_smart_token",
    ),
    path("stock_collection/<str:name>/fetch", views.stock_collection_fetch, name="stock_collection_fetch"),
    path("stock_collection/<str:name>/reset", views.stock_collection_reset, name="stock_collection_reset"),
]
