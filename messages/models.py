# from django.db import models
# from persons.models import Image


# class Message(models.Model):
#     text = models.TextField(null=True, blank=True)
#     sender = models.ForeignKey(
#         "persons.Person", models.CASCADE, related_name="sentMessages")
#     recipient = models.ForeignKey(
#         "persons.Person", models.CASCADE, related_name="receivedMessages")
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_modified = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['date_created']


# class MessageImage(Image):
#     person = models.ForeignKey(
#         Message, models.CASCADE, related_name='images')
