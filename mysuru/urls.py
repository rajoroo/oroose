from django.urls import path

from . import views

urlpatterns = [
    path("macd/", views.macd_page, name="macd"),
    path("macd/load_top_ten/", views.load_macd_page, name="load_macd_page"),
    path("macd/calculate_top_ten/", views.calculate_macd_page, name="calculate_macd_page"),
    path("stoch/", views.stoch_page, name="stoch"),
    path("stoch/load_top_ten/", views.load_stoch_page, name="load_stoch_page"),
    path("stoch/calculate_top_ten/", views.calculate_stoch_page, name="calculate_stoch_page"),
]
