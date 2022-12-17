from django.urls import path

from . import views


urlpatterns = [
    path("load_fh_view/", views.load_fh_view, name="load_fh_view"),
    path("pull_fh_api/", views.pull_fh_api, name="pull_fh_api"),
]
