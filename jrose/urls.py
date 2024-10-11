from django.urls import path

from . import views

urlpatterns = [
    path("", views.smart_buy_view, name="smart_buy"),
    path("day_page", views.day_page, name="day_page"),
]
