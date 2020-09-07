from django.contrib.auth.models import AbstractUser
from django.db import models 


class CustomUser(AbstractUser):
    likes = models.ManyToManyField(
        'posts.Post',
        related_name='liked_by'
    )

    follows = models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False
    )

    def __str__(self):
        return self.username
    
    def like(self, post):
        self.likes.add(post)
    
    def unlike(self, post):
        self.likes.remove(post)
    
    def has_liked(self, post):
        return self.likes.filter(pk=post.pk).exists()
    