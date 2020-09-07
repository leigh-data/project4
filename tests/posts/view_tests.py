import pytest
from pytest_django.asserts import assertContains, assertNotContains

from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

from posts.models import Post
from posts.views import AllPostsView, CreatePostView, FollowingPostsView, ProfilePostsView

from tests.factories import PostFactory

pytestmark = pytest.mark.django_db

User = get_user_model()

def test_index_page_view_ok(rf, posts):
    url = reverse('posts:index')
    request = rf.get(url)
    response = AllPostsView.as_view()(request)
    assert response.status_code == 200


def test_index_page_view_form_in_context(rf):
    url = reverse('posts:index')
    request = rf.get(url)
    response = AllPostsView.as_view()(request)
    assert response.context_data['form'] is not None


def test_index_page_view_ten_posts(rf, posts):
    url = reverse('posts:index')
    request = rf.get(url)
    response = AllPostsView.as_view()(request)
    posts = response.context_data['posts']
    assert len(posts) == 10
    

def test_index_page_has_second_page(rf, posts):
    url = reverse('posts:index') + "?page=2"
    request = rf.get(url)
    response = AllPostsView.as_view()(request)
    assert response.status_code == 200
    assertContains(response, "Prev")
    assertContains(response, "Next")


def test_index_page_edit_form_appears(rf, user):
    for _ in range(2):
        PostFactory(author=user)
    
    url = reverse('posts:index')
    request = rf.get(url)
    request.user = user
    response = AllPostsView.as_view()(request)

    assertContains(response, '<form class="edit-form hide"', 2)


def test_create_post_view_ok(user, rf):
    content = 'z'*126
    data = {'content': content}
    url = reverse('posts:create')
    request = rf.post(url, data)
    request.user = user
    response = CreatePostView.as_view()(request)

    assert response.status_code == 302
    assert Post.objects.filter(content=content).count() == 1


def test_create_view_anonymous_cannot_post(rf):
    content = 'z'*126
    data = {'content': content}
    url = reverse('posts:create')
    request = rf.post(url, data)
    request.user = AnonymousUser()
    response = CreatePostView.as_view()(request)

    assert response.status_code == 302
    assert Post.objects.filter(content=content).count() == 0


def test_create_view_empty_data_fail(rf, user):
    data = {}
    url = reverse('posts:create')
    request = rf.post(url, data)
    request.user = user
    response = CreatePostView.as_view()(request)

    assert response.status_code == 200


def test_profile_view_queryset(user, posts, rf):
    other_user = User.objects.exclude(pk=user.pk).first()
    url = reverse('posts:profile', kwargs={'username': other_user.username})
    request = rf.get(url)
    request.user = user
    view = ProfilePostsView(kwargs={'username': other_user.username})
    view.request = request
    qs = view.get_queryset()
    assert qs.count() == other_user.posts.count()


def test_profile_view_get_context_data(user, posts, rf):
    url = reverse('posts:profile', kwargs={'username': user.username})
    request = rf.get(url)
    request.user = user
    response = ProfilePostsView.as_view()(request, username=user.username)
    
    assert response.context_data['profile_user'] == user
    assert response.context_data['following'] == False
    assert response.context_data['profile'] == True


def test_profile_view_own_profile_has_no_follow_button(user, rf):
    url = reverse('posts:profile', kwargs={'username': user.username})
    request = rf.get(url)
    request.user = user
    response = ProfilePostsView.as_view()(request, username=user.username)

    assertNotContains(response, '<button class="follow-button btn')


def test_profile_view_own_profile_has_no_follow_button_anonymous_user(rf, posts):
    other_user = User.objects.all().first()
    print(other_user)
    url = reverse('posts:profile', kwargs={'username': other_user.username})

    request = rf.get(url)
    request.user = AnonymousUser()
    response = ProfilePostsView.as_view()(request,username=other_user.username)

    assertNotContains(response, '<button class="follow-button btn')


def test_profile_view_other_user_has_button(user, posts, rf):
    other_user = User.objects.exclude(pk=user.pk).first()
    url = reverse('posts:profile', kwargs={'username': other_user.username})
    request = rf.get(url)
    request.user = user
    response = ProfilePostsView.as_view()(request, username=other_user.username)

    assertContains(response, '<button class="follow-button btn')


def test_following_view_queryset(user, posts, rf):
    url = reverse('posts:following')
    other_users = User.objects.exclude(username=user.username)
    for other_user in other_users:
        user.follows.add(other_user)
    
    request = rf.get(url)
    request.user = user
    view = FollowingPostsView()
    view.request = request
    qs = view.get_queryset()

    assert qs.count() == Post.objects.count()


def test_following_view_has_third_page_has_five_posts(rf, user, posts):
    url = reverse('posts:index') + "?page=3"
    request = rf.get(url)
    request.user = user
    response = AllPostsView.as_view()(request)
    posts = response.context_data['posts']
    assert len(posts) == 5
