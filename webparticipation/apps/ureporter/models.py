import datetime
import bcrypt
from django.db import models
from django.utils import timezone
from random import randint


def generate_token():
    return str(randint(1000, 9999))


class Ureporter(models.Model):

    def set_uuid(self, uuid):
        self.uuid = uuid
        self.save()

    def set_email(self, email):
        self.email = email
        self.save()

    def set_password(self, password):
        password = password.encode('utf-8')
        salt = bcrypt.gensalt().encode('utf-8')
        self.password = bcrypt.hashpw(password, salt)
        self.save()

    def invalidate_token(self):
        self.token = 0
        self.save()

    def is_user_valid(self, password):
        return bcrypt.hashpw(password, self.password) == self.password

    def token_has_expired(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    uuid = models.CharField(max_length=36)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    token = models.IntegerField(default=generate_token)
    pub_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.uuid
