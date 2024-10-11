from django.urls import path

from . import views

urlpatterns = [
    path("", views.smart_buy_view, name="smart_buy"),
]
