from dataclasses import field
from django.forms import ValidationError
from rest_framework import serializers

from .models import Post, Comment, Like, SavedPost
from accounts.serializer import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    comment_by = UserSerializer(read_only=True)
    class Meta:
        model=Comment
        fields = ("id", 'post', 'comment', 'comment_by')

class LikeSerializer(serializers.ModelSerializer):
    liked_by = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ("id","post", "liked_by")
        extra_kwargs = {
            "post": {"read_only": True}
        }

class PostSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    class Meta:
        model= Post
        fields = ("id", "img", "posted_at", "caption", "owner","comments", "likes")

    def validate(self, attrs):
        img = attrs.get("img")
        if not img:
            raise ValidationError({"img": "This is required for uploading post."})
        return super().validate(attrs)

    # def save(self):
    #     user = self.context["user"]
    #     self.validated_data["owner"] = user
    #     return super().save()cls

class SavedPostSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    class Meta:
        model = SavedPost
        fields= ("id", 'post', 'user')


    