from django.contrib.auth.hashers import make_password
from django.forms import ValidationError
from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    profile_pic = serializers.ImageField(required=False, allow_empty_file=True)
    class Meta:
        model = User
        fields = ["id", "email", "username", "password", "full_name", "profile_pic"]
        extra_kwargs = {"password": {"write_only": True}, "url": {"lookup_field": 'username'}}

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

# class UpdateUserSerializer(serializers.ModelSerializer):
#     profile_pic = serializers.ImageField(required=False, allow_empty_file=True)
#     class Meta:
#         model = User
#         fields = ("email", "username", "full_name", "profile_pic")

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


