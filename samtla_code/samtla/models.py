from __future__ import unicode_literals

from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

import datetime
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

class Query_Stats(models.Model):
    query = models.TextField(blank=True)
    date_time = models.IntegerField(null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)
    user = models.TextField(blank=True)
    
    def __str__(self):
        return '%s %s %s %s' %(self.query, str(self.date_time), str(self.count), self.user)

    class Meta:
        db_table = u'Query_Stats'

class User_Feedback(models.Model):
    date_time = models.DateField(("Date"), auto_now_add=True)
    user = models.TextField(blank=True)
    topic = models.TextField(blank=True)
    message = models.TextField(blank=True)
    query = models.TextField(blank=True)

    def __str__(self):
        return '%s %s %s %s' %(self.date_time, str(self.topic), str(self.message), self.user)

    class Meta:
        db_table = u'User_Feedback'

class User_Registration(models.Model):
    date_time = models.DateField(("Date"), auto_now_add=True)
    fullname = models.TextField(blank=True)
    username = models.TextField(blank=True)
    email = models.TextField(blank=True)
    password = models.TextField(blank=True)
    
    def __str__(self):
        return '%s %s %s %s' %(self.date_time, str(self.topic), str(self.message), self.user)

    class Meta:
        db_table = u'User_Registration'


class UserActivity(models.Model):    
    user = models.ForeignKey(User, null=True, blank=True, db_index=True, related_name='+')
    timestamp = models.DateTimeField(help_text="Date Request started processing", auto_now_add=True, db_index=True)
    URL = models.CharField(max_length=256, blank=True,null=True)
    arg = models.CharField(max_length=800, db_index=True)


