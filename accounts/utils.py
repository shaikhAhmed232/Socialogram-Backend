from django.utils import timezone
import os
from rest_framework_simplejwt.tokens import RefreshToken

def upload_img_url(instance, filename):
    date = timezone.now()
    path = os.path.join("user-pic", instance.username, str(date.year), str(date.month), str(date.day), filename)
    return path

def get_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token), 
    }

def convert_to_seconds(timedelta):
    seconds = timedelta.seconds
    if not seconds:
        seconds = timedelta.days * 3600 * 24
    return seconds


    