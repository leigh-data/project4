import pytest
from pytest_django.asserts import assertContains

from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory

from posts.models import Post
from api.views import PostRetrieveUpdateView, PostListCreateView, PostLikeAPIView, UserFollowAPIView

from tests.factories import UserFactory, PostFactory

pytestmark = pytest.mark.django_db
User = get_user_model()


def test_get_posts_unauthenticated(api_rf, posts):
    url = reverse('api:posts')
    request = api_rf.get(url)
    response = PostListCreateView.as_view()(request)

    assert response.status_code == 200


def test_get_post(api_rf, post):
    url = reverse('api:post', kwargs={'pk': post.pk})
    request = api_rf.get(url)
    response = PostRetrieveUpdateView.as_view()(request, pk=post.pk)

    assert response.status_code == 200

def test_update_post(api_rf, user):
    post = user.posts.create(content='a'*100)
    content = 'this is a journey into sound!'
    url = reverse('api:post', kwargs={'pk':post.pk})
    data = {'content': content}
    request = api_rf.put(url, data)
    request.user = user
    response = PostRetrieveUpdateView.as_view()(request, pk=post.pk)

    assert user.posts.get(pk=post.pk).content == content


def test_post_like_success(api_rf, user):
    new_user = UserFactory()
    liked_post = PostFactory(author=new_user)
    
    url = reverse('api:like', kwargs={'pk': liked_post.pk})
    request = api_rf.post(url)
    request.user = user
    response = PostLikeAPIView.as_view()(request, pk=liked_post.pk)

    assert user.has_liked(liked_post)


def test_post_like_failure(api_rf, user):

    url = reverse('api:like', kwargs={'pk': 666})
    request = api_rf.post(url)
    request.user = user
    response = PostLikeAPIView.as_view()(request, pk=666)

    assert response.status_code == 400

def test_post_unlike_success(api_rf, user):
    new_user = UserFactory()
    liked_post = PostFactory(author=new_user)
    user.like(liked_post)
    assert user.has_liked(liked_post)

    url = reverse('api:like', kwargs={'pk': liked_post.pk})
    request = api_rf.delete(url)
    request.user = user
    response = PostLikeAPIView.as_view()(request, pk=liked_post.pk)

    assert not user.has_liked(liked_post)


def test_post_unlike_failure(api_rf, user):

    url = reverse('api:like', kwargs={'pk': 666})
    request = api_rf.delete(url)
    request.user = user
    response = PostLikeAPIView.as_view()(request, pk=666)

    assert response.status_code == 400


def test_user_follow_success(api_rf, user):
    new_user = UserFactory()

    url = reverse('api:follow', kwargs={'pk': new_user.pk})
    request = api_rf.post(url)
    request.user = user
    response = UserFollowAPIView.as_view()(request, pk=new_user.pk)

    assert user.follows.get(pk=new_user.pk)


def test_user_follow_failure(api_rf, user):
    url = reverse('api:follow', kwargs={'pk': 666})
    request = api_rf.post(url)
    request.user = user
    response = UserFollowAPIView.as_view()(request, pk=666)

    with  pytest.raises(User.DoesNotExist):
        assert not user.follows.get(pk=666)


def test_user_follow_failure_cannot_follow_yourself(api_rf, user):
    url = reverse('api:follow', kwargs={'pk': user.pk})
    request = api_rf.post(url, format='json')
    request.user = user
    response = UserFollowAPIView.as_view()(request, pk=user.pk)

    assert response.status_code == 400
    assert "You cannot follow yourself" in response.data

def test_user_unfollow_success(api_rf, user):
    new_user = UserFactory()
    user.follows.add(new_user)

    url = reverse('api:follow', kwargs={'pk': new_user.pk})
    request = api_rf.delete(url)
    request.user = user
    response = UserFollowAPIView.as_view()(request, pk=new_user.pk)
    
    with pytest.raises(User.DoesNotExist):
        assert not user.follows.get(pk=new_user.pk)


def test_user_unfollow_failure(api_rf, user):
    url = reverse('api:follow', kwargs={'pk': 666})
    request = api_rf.delete(url)
    request.user = user
    response = UserFollowAPIView.as_view()(request, pk=666)

    with pytest.raises(User.DoesNotExist):
        assert user.follows.get(pk=666)
        assert 'User does not exist' in response.data
