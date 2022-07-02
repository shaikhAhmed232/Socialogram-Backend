from wsgiref import validate
from xml.dom import ValidationErr
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    profile_pic = serializers.ImageField(required=False, allow_empty_file=True)
    class Meta:
        model = User
        fields = ["email", "username", "password", "full_name", "profile_pic"]
        extra_kwargs = {"password": {"write_only": True}}


    def update(self, instance, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        full_name = validated_data["full_name"]

        instance.username = username
        instance.email = email
        instance.full_name = full_name
        instance.save()
        return instance
