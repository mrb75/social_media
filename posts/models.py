from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
from django.utils.translation import gettext as _
from persons.models import Image


class Post(models.Model):

    person = models.ForeignKey(
        "persons.Person", models.CASCADE, related_name="posts")
    caption = models.TextField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True, max_length=2, validators=[
                            MinValueValidator(-90), MaxValueValidator(90)])
    long = models.FloatField(null=True, blank=True, max_length=2, validators=[
        MinValueValidator(-90), MaxValueValidator(90)])
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_created']
        verbose_name = _("")
        verbose_name_plural = _("s")

    def __str__(self):
        return self.name


class PostImage(Image):
    post = models.ForeignKey(
        Post, models.CASCADE, related_name='images')


class Comment(models.Model):
    post = models.ForeignKey(Post, models.CASCADE, related_name="comments")
    parent = models.ForeignKey(
        "self", models.CASCADE, related_name="replies", null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_created']
