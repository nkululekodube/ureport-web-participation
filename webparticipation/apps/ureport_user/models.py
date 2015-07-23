import datetime
import bcrypt
from django.db import models
from django.utils import timezone
from random import randint


class UreportUser(models.Model):
    def generate_token():
        return str(randint(1000, 9999))

    def token_has_expired(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def invalidate_token(self):
        self.token = 0
        self.save()

    def activate_user(self):
        self.active = True
        self.save()

    def set_password(self, password):
        password = password.encode('utf-8')
        salt = bcrypt.gensalt().encode('utf-8')
        self.password = bcrypt.hashpw(password, salt)
        self.save()

    def is_user_valid(self, password):
        return bcrypt.hashpw(password, self.password) == self.password

    email = models.EmailField(max_length=255, null=False)
    password = models.CharField(max_length=255, null=False)
    active = models.BooleanField(default=False)
    token = models.IntegerField(null=False, default=generate_token())
    uuid = models.CharField(max_length=36)
    pub_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.uuid
