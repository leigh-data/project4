from datetime import datetime, timezone

import factory
from factory import fuzzy

from posts.models import Post
from users.models import CustomUser


class UserFactory(factory.django.DjangoModelFactory):
    username = fuzzy.FuzzyText(length=12)
    class Meta:
        model = CustomUser


class PostFactory(factory.django.DjangoModelFactory):
    created = fuzzy.FuzzyDateTime(datetime(2020, 1, 1, tzinfo=timezone.utc))
    author = factory.SubFactory(UserFactory)
    content = fuzzy.FuzzyText(length=126)
    class Meta:
        model = Post


class UserWithPostsFactory(UserFactory):
    @factory.post_generation
    def posts(user, create, number_of_posts, **kwargs):
        if not create: return
        if number_of_posts is None: number_of_posts = 10

        for n in range(number_of_posts):
            PostFactory(author=user)
