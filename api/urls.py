from django.urls import path
from api.views import PostRetrieveUpdateView, PostListCreateView, PostLikeAPIView, UserFollowAPIView

app_name = 'api'

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='posts'),
    path('posts/<int:pk>/', PostRetrieveUpdateView.as_view(), name='post'),
    path('posts/<int:pk>/like/', PostLikeAPIView.as_view(), name='like'),
    path('users/<int:pk>/follow/', UserFollowAPIView.as_view(), name='follow')
]
