from django.utils import timezone
import os

def post_img_url(instance, filename):
    date = timezone.now()
    path = os.path.join("posts", instance.owner.username, str(date.year), str(date.month), str(date.day), filename)
    return path