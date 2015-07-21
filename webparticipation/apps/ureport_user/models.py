import datetime
from django.db import models
from django.utils import timezone

class UreportUser(models.Model):
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    active = models.BooleanField()
    token = models.IntegerField(max_length=3)
    user_id = models.CharField(max_length=13)
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):
        return self.user_id
    def token_has_expired(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    def invalidate_token(self):
        self.token = None
    def activate_user(self):
        self.active = True
