from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    liked = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'created', 'liked', 'like_count']
    
    def get_liked(self, instance):
        request = self.context.get('request')
        
        if request is None:
            return False
        
        if not request.user.is_authenticated:
            return False
        
        return request.user.has_liked(instance)
    
    def get_like_count(self, instance):
        return instance.liked_by.count()


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.StringRelatedField(many=True, read_only=True)
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'following', 'posts']

    def get_following(self, instance):
        request = self.context.get('request')

        if request is None:
            return False

        if not request.user.is_authenticated:
            return False

        follower = request.user
        followee = instance
        return follower.follows.filter(pk=followee.pk).exists()
