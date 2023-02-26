from django.urls import path

from . import views


urlpatterns = [
    path("", views.mysuru_page, name="mysuru"),
    path("content/", views.load_mysuru_content, name="mysuru_content"),
    path("mysuru_load_top_ten_api/", views.mysuru_load_top_ten_api, name="mysuru_load_top_ten_api"),
    path("mysuru_get_accepted_api/", views.mysuru_get_accepted_api, name="mysuru_get_accepted_api"),
    path("mysuru_panic_pull/", views.mysuru_panic_pull, name="mysuru_panic_pull"),
]
