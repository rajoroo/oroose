from django.urls import path
from . import views

urlpatterns = [
    path('load_five_hundred/', views.load_five_hundred, name='load_500'),
    path('pull_five_hundred/', views.pull_five_hundred, name='pull_500'),
    path('get_zero_value/', views.get_zero_value, name='zero'),
    path('load_five_hundred_zero/', views.load_five_hundred_zero, name='zero'),
    path('', views.bengaluru_page, name='bengaluru'),
]
