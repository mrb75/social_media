from celery import shared_task
from .models import PostImage
import os


@shared_task()
def delete_removed_image_file(image):
    path = str(image.path)
    if path:
        os.remove(path)
