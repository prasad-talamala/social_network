from django.contrib.auth.models import User
from django.db import models


class PostsModel(models.Model):
    heading = models.CharField(max_length=200)
    message = models.TextField(max_length=4000, blank=True)
    post_image = models.ImageField(upload_to="posts/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)


class SocialConnectivity(models.Model):
    follower = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
