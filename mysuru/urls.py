from django.urls import path

from . import views

urlpatterns = [
    path("macd/", views.macd_page, name="macd"),
    path("macd/load_top_ten/", views.load_macd_page, name="load_macd_page"),
    path("macd/calculate_top_ten/", views.calculate_macd_page, name="calculate_macd_page"),
]
