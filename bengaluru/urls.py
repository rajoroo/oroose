from django.urls import path

from . import views

urlpatterns = [
    path("load_fh_view/", views.load_fh_view, name="load_fh_view"),
    path("pull_fh_api/", views.pull_fh_api, name="pull_fh_api"),
    path("evaluate_fh_zero/", views.evaluate_fh_zero, name="evaluate_fh_zero"),
    path("load_fh_zero_view/", views.load_fh_zero_view, name="load_fh_zero_view"),
    path("process_fh_zero_api/", views.process_fh_zero_api, name="process_fh_zero_api"),
    path("", views.bengaluru_page, name="bengaluru"),
]
