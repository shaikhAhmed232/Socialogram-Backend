from dataclasses import field
from django.forms import ValidationError
from rest_framework import serializers

from .models import Post, Comment
from accounts.serializer import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    comment_by = UserSerializer()
    class Meta:
        model=Comment
        fields = ('post', 'comment', 'comment_by')

class PostSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model= Post
        fields = ("id", "img", "posted_at", "caption", "owner", "comments")

    def validate(self, attrs):
        img = attrs.get("img")
        if not img:
            raise ValidationError({"img": "This is required for uploading post."})
        return super().validate(attrs)

    # def save(self):
    #     user = self.context["user"]
    #     self.validated_data["owner"] = user
    #     return super().save()cls


    