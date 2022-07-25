from dataclasses import field
from django.forms import ValidationError
from rest_framework import serializers

from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model= Post
        fields = ("id", "img", "posted_at", "caption", "owner")

    def validate(self, attrs):
        img = attrs.get("img")
        if not img:
            raise ValidationError({"img": "This is required for uploading post."})
        return super().validate(attrs)

    # def save(self):
    #     user = self.context["user"]
    #     self.validated_data["owner"] = user
    #     return super().save()