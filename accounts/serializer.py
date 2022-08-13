from dataclasses import fields
from django.contrib.auth.hashers import make_password
from django.forms import ValidationError
from rest_framework import serializers

from .models import User, Contact

# Serializer for serializing contact model's following_user_id field.
class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contact
        fields=('id', 'following_user_id',)

# Serializer for serializing Contact model's user_id field.
class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contact
        fields=('id', 'user_id',)

# Serializer for serializing user Model.
class UserSerializer(serializers.ModelSerializer):
    profile_pic = serializers.ImageField(required=False, allow_empty_file=True)
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "username", "password", "full_name", "profile_pic", "followers", "following"]
        extra_kwargs = {"password": {"write_only": True}, "url": {"lookup_field": 'username'}}

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    # list of users who is followed by current user.
    def get_following(self, obj):
        following = obj.following.all()
        return FollowingSerializer(following, many=True).data

    # list of users who is following current user.
    def get_followers(self, obj):
        return FollowerSerializer(obj.followers.all(), many=True).data
# class UpdateUserSerializer(serializers.ModelSerializer):
#     profile_pic = serializers.ImageField(required=False, allow_empty_file=True)
#     class Meta:
#         model = User
#         fields = ("email", "username", "full_name", "profile_pic")

# Serializer for changing current user's password
class ChangeUserPasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    conf_new_pass = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields=('old_password', "new_password", "conf_new_pass")

    def validate(self, attrs):
        password = attrs.get('new_password')
        conf_new_pass  = attrs.get('conf_new_pass')

        if password != conf_new_pass:
            raise ValidationError('Both new passwords are not matching!')

        return super().validate(attrs)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise ValidationError("Password is not matching with current password.")
        return value

    def update(self, instance, validated_data):        
        instance.set_password(validated_data["new_password"])
        instance.save()
        return instance

# Contact model serializer
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contact
        fields = "__all__"




    


