from django.urls import path
from . import views

urlpatterns = [
    path("load_five_hundred/", views.load_fh, name="load_fh"),
    path("pull_five_hundred/", views.pull_fhz, name="pull_fh"),
    path("get_zero_value/", views.analyse_fhz, name="analyse_fhz"),
    path("load_five_hundred_zero/", views.load_fhz, name="load_fhz"),
    path(
        "process_five_hundred_zero//<int:object_id>/",
        views.process_fhz,
        name="process_fhz",
    ),
    path("", views.bengaluru_page, name="bengaluru"),
]
