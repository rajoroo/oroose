from django.urls import path
from . import views

urlpatterns = [
    path('load-500/', views.load_five_hundred, name='load-500'),
    path('', views.docs, name='bengaluru'),
]
