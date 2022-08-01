from distutils.command.upload import upload
from django.db import models
from django.contrib.auth import get_user_model

from .utils import post_img_url

User = get_user_model()

class CurrentUsersPosts(models.QuerySet):
    def get_current_user_posts(self, user=None):
        return self.filter(owner = user)

# Create your models here.
class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    img = models.ImageField(upload_to=post_img_url, default="default.jpg", max_length=200)
    caption = models.CharField(max_length=100, null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True, blank=True)

    objects = models.Manager()
    current_user_posts = CurrentUsersPosts.as_manager()

    class Meta:
        ordering = ("-posted_at",)

    def __str__(self):
        return f"{self.img} posted by {self.owner} at {self.posted_at}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", default=3)
    comment = models.CharField(max_length=300)
    comment_by = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="user_comments", default=8)

    def __str__(self):
        return f"{self.comment_by.username} commented {self.comment} on {self.post.img}"

    def get_comment_user(self):
        return self.comment_by
