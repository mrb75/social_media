from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.translation import gettext as _
# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=30)
    phone_code = models.CharField(max_length=5)


class Person(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'Male', _('مرد')
        FEMALE = 'Female', _('زن')
        NOTHING = 'Nothing', _('هیچکدام')
    country = models.ForeignKey(Country, models.CASCADE,
                                related_name='persons', null=True, blank=True)
    relegion = models.CharField(null=True, blank=True, max_length=50)
    date_modified = models.DateTimeField(auto_now=True)
    birth_date = models.DateField(null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    gender = models.CharField(choices=Gender.choices,
                              default=Gender.NOTHING, max_length=10)
    credit = models.BigIntegerField(default=0)
    point = models.IntegerField(default=0)


class Image(models.Model):
    path = models.ImageField(upload_to='files/images')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['date_created']


class PersonImage(Image):
    person = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE, related_name='images')


class Notification(models.Model):
    person = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE,
                               related_name='notifications')
    is_news = models.BooleanField(default=False)
    text = models.TextField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_created']


class Ticket(models.Model):
    class Type(models.TextChoices):
        MANAGEMENT = 'Management', _('مدیریت')
        MARKETING = 'Marketing', _('فروش و بازاریابی')
        SUPPORT = 'Support', _('پشتیبانی')
        COMPLAINS = 'Complains', _('شکایات')
        SUGGESTION = 'Suggestions', _('انتقادات و پیشنهادات')

    class State(models.TextChoices):
        CLOSED = 'Closed', _('بسته شده')
        OPEN = 'Pending', _('در حال بررسی')
        INIT = 'Waiting', _('در انتظار بررسی')

    message_type = models.CharField(
        choices=Type.choices, default=Type.SUGGESTION, max_length=30)
    subject = models.CharField(max_length=255)
    person = models.ForeignKey(settings.AUTH_USER_MODEL,
                               models.CASCADE, related_name='tickets')
    status = models.CharField(
        choices=State.choices, default=State.INIT, max_length=30)
    text = models.TextField(max_length=20000)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_created']


class RequestLog(models.Model):
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name='requestLogs', null=True)
    ip_address = models.GenericIPAddressField()
    referer = models.CharField(max_length=255, null=True)
    user_agent = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=100, null=True)
    method = models.CharField(max_length=10)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_created']
