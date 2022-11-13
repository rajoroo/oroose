from django.urls import path

from . import views

urlpatterns = [
    path("load_fh_view/", views.load_fh_view, name="load_fh_view"),
    path("pull_fh_api/", views.pull_fh_api, name="pull_fh_api"),
    # Bengaluru
    path("fhz_uptrend_record/<int:pk>", views.EditFhzUptrend.as_view(), name="fhz_uptrend_record"),
    path("load_fhz_uptrend_view/", views.load_fhz_uptrend_view, name="fhz_uptrend_view"),
    path("load_fhz_uptrend_error_view/", views.load_fhz_uptrend_error_view, name="fhz_uptrend_error_view"),
    path("load_fhz_uptrend_sold_view/", views.load_fhz_uptrend_sold_view, name="fhz_uptrend_sold_view"),
    # Mysuru
    path("fhz_downtrend_record/<int:pk>", views.EditFhzDowntrend.as_view(), name="fhz_downtrend_record"),
    path("load_fhz_downtrend_view/", views.load_fhz_downtrend_view, name="fhz_downtrend_view"),
    path("load_fhz_downtrend_error_view/", views.load_fhz_downtrend_error_view, name="fhz_downtrend_error_view"),
    path(
        "load_fhz_downtrend_purchased_view/",
        views.load_fhz_downtrend_purchased_view,
        name="fhz_downtrend_purchased_view",
    ),
    path("", views.bengaluru_page, name="bengaluru"),
    path("mysuru/", views.mysuru_page, name="mysuru"),
]
