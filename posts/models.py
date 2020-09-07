from django.db import models
from django.contrib.auth import get_user_model

from django_extensions.db.models import TimeStampedModel


User = get_user_model()


class Post(TimeStampedModel):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=126)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.content
    
    def like_count(self):
        return self.liked_by.count()
