from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    device_token = models.CharField(max_length=500)