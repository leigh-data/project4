from django.contrib.auth import get_user_model

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError

from posts.models import Post
from api.serializers import PostSerializer, UserSerializer
from api.permissions import IsAuthorOrReadOnly

User = get_user_model()

class PostRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = PostSerializer


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostLikeAPIView(APIView):
    serializer_class = PostSerializer

    def delete(self, request, pk):
        serializer_context = {'request': request}
        user = self.request.user

        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise ValidationError('Post does not exist')

        user.unlike(post)
        serializer = self.serializer_class(post, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        serializer_context = {'request': request}
        user = self.request.user

        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise ValidationError('Post does not exist')

        user.like(post)
        serializer = self.serializer_class(post, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserFollowAPIView(APIView):
    serializer_class = UserSerializer

    def delete(self, request, pk):
        follower = request.user

        try:
            followee = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise ValidationError('User does not exist')

        follower.follows.remove(followee)
        serializer = self.serializer_class(followee, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        follower = request.user

        try:
            followee = User.objects.get(pk=pk)

        except User.DoesNotExist:
            raise ValidationError('User does not exist')

        if follower.pk is followee.pk:
            raise ValidationError("You cannot follow yourself")

        follower.follows.add(followee)
        
        serializer = self.serializer_class(
            followee, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
