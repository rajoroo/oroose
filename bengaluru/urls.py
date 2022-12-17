from django.urls import path

from . import views

urlpatterns = [
    path("fhz_uptrend_record/<int:pk>", views.EditFhzUptrend.as_view(), name="fhz_uptrend_record"),
    path("load_fhz_uptrend_view/", views.load_fhz_uptrend_view, name="fhz_uptrend_view"),
    path("load_fhz_uptrend_error_view/", views.load_fhz_uptrend_error_view, name="fhz_uptrend_error_view"),
    path("load_fhz_uptrend_sold_view/", views.load_fhz_uptrend_sold_view, name="fhz_uptrend_sold_view"),
    path("", views.bengaluru_page, name="bengaluru"),
]
