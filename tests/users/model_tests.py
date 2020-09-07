import pytest

from users.models import CustomUser

pytestmark = pytest.mark.django_db


def test_create_user(user):
    assert user.username == "testuser"
    assert user.email == "tester@example.com"
    assert user.is_staff == False
    assert user.is_superuser == False


def test_create_superuser():
    user = CustomUser.objects.create_superuser(
        username="clarkekent", password="testpass123", email="clarke@dailyplanet.com")

    assert user.username == "clarkekent"
    assert user.email == "clarke@dailyplanet.com"
    assert user.is_staff == True
    assert user.is_superuser == True


def test_user__str__(user):
    assert str(user) == "testuser"

def test_user_like_post(user, post):
    user.like(post)
    assert user.has_liked(post)

def test_user_unlike_post(user, post):
    user.like(post)
    user.unlike(post)
    assert not user.has_liked(post)
