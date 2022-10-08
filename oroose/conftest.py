from django.test import Client
from django.contrib.auth.models import User

import pytest


@pytest.fixture(scope="class")
def login_user(request):
   request.cls.client = Client()
   request.cls.user = User.objects.create_user('john', 'lennon@xing.com', 'johnpassword')
   request.cls.client.force_login(request.cls.user)


