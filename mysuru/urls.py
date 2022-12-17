from django.urls import path

from . import views

urlpatterns = [
    path("fhz_downtrend_record/<int:pk>", views.EditFhzDowntrend.as_view(), name="fhz_downtrend_record"),
    path("load_fhz_downtrend_view/", views.load_fhz_downtrend_view, name="fhz_downtrend_view"),
    path("load_fhz_downtrend_error_view/", views.load_fhz_downtrend_error_view, name="fhz_downtrend_error_view"),
    path("load_fhz_downtrend_purc_view/", views.load_fhz_downtrend_purc_view, name="fhz_downtrend_purc_view"),
    path("trigger_downtrend_panic_pull/", views.trigger_downtrend_panic_pull, name="trigger_downtrend_panic_pull"),
    path("", views.mysuru_page, name="mysuru"),
]
