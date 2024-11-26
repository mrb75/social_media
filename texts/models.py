from django.db import models
from persons.models import Image


class Text(models.Model):
    content = models.TextField(null=True, blank=True)
    sender = models.ForeignKey(
        "persons.Person", models.CASCADE, related_name="sentTexts")
    recipient = models.ForeignKey(
        "persons.Person", models.CASCADE, related_name="receivedTexts")
    parent = models.ForeignKey(
        "self", models.CASCADE, related_name="replies", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_created']


class TextImage(Image):
    person = models.ForeignKey(
        Text, models.CASCADE, related_name='images')
