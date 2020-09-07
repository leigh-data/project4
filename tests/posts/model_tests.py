import pytest

from posts.models import Post

pytestmark = pytest.mark.django_db


def test_create_post(user, post):
    content = 'x'*126
    assert post.content == content
    assert post.author == user


def test__str__(post):
    content = 'x'*126
    assert str(post) == content


def test_like_count_none(post):
    assert not post.like_count()

def test_like_count_one(user, post):
    user.like(post)
    assert post.like_count() == 1
