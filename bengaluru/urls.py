from django.urls import path

from . import views

urlpatterns = [
    path("fhz_uptrend_record/<int:pk>", views.EditFhzUptrend.as_view(), name="fhz_uptrend_record"),
    path("trigger_uptrend_panic_pull/", views.trigger_uptrend_panic_pull, name="trigger_uptrend_panic_pull"),
    path("content/", views.load_bengaluru_content, name="bengaluru_content"),
    path("", views.bengaluru_page, name="bengaluru"),
]
