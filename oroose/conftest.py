import pytest
from django.contrib.auth.models import User
from django.test import Client


@pytest.fixture(scope="class")
def login_user(request):
    request.cls.client = Client()
    request.cls.user = User.objects.create_user("john", "lennon@xing.com", "johnpassword")
    request.cls.client.force_login(request.cls.user)
