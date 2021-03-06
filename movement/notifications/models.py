from __future__ import unicode_literals

import os
import json

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db import models

import requests


class Notification(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    
    cohort = models.ForeignKey(Group)
    
    status = models.BooleanField(default=False)
    
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '%s' % ( self.title, )


@receiver(post_save, sender=Notification, dispatch_uid="issue_push_notification")
def issue_push_notification(sender, instance, **kwargs):
    
    print instance.cohort

    users = User.objects.filter(groups=instance.cohort)
    
    print users
    
    tokens = [ getattr(user.account, 'device_token', '') for user in users ]
    
    print tokens
    
    response = requests.post(
        'https://api.ionic.io/push/notifications',
        headers={
          "Content-Type": "application/json",
          "Authorization": "Bearer " + os.environ.get("IONIC_TOKEN")
        }, 
        data= json.dumps({
                "tokens": tokens,
                "profile": "push_notifications",
                "notification": {
                    "title": instance.title,
                    "message": instance.message
                }
        }))
    print response.text
