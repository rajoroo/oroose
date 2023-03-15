from django.urls import path

from . import views


urlpatterns = [
    path("", views.mysuru_page, name="mysuru"),
    path("mysuru_load_top_ten/", views.mysuru_load_top_ten, name="mysuru_load_top_ten"),
    path("mysuru_calculate_top_ten/", views.mysuru_calculate_top_ten, name="mysuru_calculate_top_ten"),
]
