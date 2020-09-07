from django.urls import path

from .views import *

app_name = "posts"

urlpatterns = [
    path('', AllPostsView.as_view(), name='index'),
    path('following/', FollowingPostsView.as_view(), name='following'),
    path('create/', CreatePostView.as_view(), name='create'),
    path('<str:username>/', ProfilePostsView.as_view(), name='profile'),
]
