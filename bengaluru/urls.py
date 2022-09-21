from django.urls import path
from . import views

urlpatterns = [
    path('load_five_hundred/', views.load_five_hundred, name='load_fh'),
    path('pull_five_hundred/', views.pull_five_hundred, name='pull_fh'),
    path('get_zero_value/', views.get_zero_value, name='analyse_fhz'),
    path('load_five_hundred_zero/', views.load_five_hundred_zero, name='load_fhz'),
    path('', views.bengaluru_page, name='bengaluru'),
]
