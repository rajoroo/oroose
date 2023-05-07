"""oroose URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from home import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", views.home_page, name="home"),
    path("mysuru/", include("mysuru.urls")),
    path("configuration_page/", views.configuration_page, name="configuration"),
    path("config_file_upload/", views.upload_config_file, name="upload_config_file"),
    path("generate_smart_token/", views.generate_smart_token, name="generate_smart_token"),
    path("reset_configuration/", views.reset_configuration, name="reset_configuration"),
]
