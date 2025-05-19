from django.urls import path

from . import views

urlpatterns = [
    path("week_page", views.week_page, name="week_page"),
    path("day_page", views.day_page, name="day_page"),
    path("hr_page", views.hr_page, name="hr_page"),
    path("potential_page", views.potential_page, name="potential_page"),
    path("stoch_page", views.stoch_page, name="stoch_page"),
    path("rsi_page", views.rsi_page, name="rsi_page"),

]
