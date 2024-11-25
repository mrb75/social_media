from django.dispatch import Signal, receiver
from django.db.models.signals import post_delete
from .models import PostImage, Post
from .tasks import delete_removed_image_file


@receiver(post_delete, sender=PostImage)
def remove_image_file(sender, **kwargs):
    delete_removed_image_file(kwargs["instance"])
