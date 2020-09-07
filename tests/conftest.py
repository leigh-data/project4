import pytest

from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory

from .factories import UserWithPostsFactory

pytestmark = pytest.mark.django_db

User = get_user_model()


@pytest.fixture
def user(scope="session"):
    return User.objects.create_user(username="testuser", password="testpass123", email="tester@example.com")


@pytest.fixture
def post(user, scope="session"):
    content = 'x'*126
    return user.posts.create(content=content)


@pytest.fixture
def posts(scope="module"):
    for _ in range(5):
        UserWithPostsFactory()

@pytest.fixture
def api_rf():
    rf = APIRequestFactory()
    yield rf
