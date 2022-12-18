from django.urls import path

from . import views

urlpatterns = [
    path("fhz_downtrend_record/<int:pk>", views.EditFhzDowntrend.as_view(), name="fhz_downtrend_record"),
    path("trigger_downtrend_panic_pull/", views.trigger_downtrend_panic_pull, name="trigger_downtrend_panic_pull"),
    path("content/", views.load_mysuru_content, name="mysuru_content"),
    path("", views.mysuru_page, name="mysuru"),
]
