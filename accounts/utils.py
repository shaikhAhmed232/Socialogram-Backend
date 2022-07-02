from datetime import datetime
import os
from rest_framework_simplejwt.tokens import RefreshToken

def upload_img_url(instance, filename):
    ddd = datetime.now
    path = os.path.join("user-pic", instance.username, ddd.date(), filename)
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


    