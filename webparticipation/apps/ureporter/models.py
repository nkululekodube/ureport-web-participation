import datetime
from django.db import models
from django.utils import timezone
from random import randint
from django.conf import settings


def generate_token():
    return str(randint(1000, 9999))


class Ureporter(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    uuid = models.CharField(max_length=36)
    urn_tel = models.CharField(max_length=13)
    token = models.IntegerField(default=generate_token)

    def set_uuid(self, uuid):
        self.uuid = uuid
        self.save()

    def invalidate_token(self):
        self.token = 0
        self.save()

    def token_has_expired(self):
        return self.user.date_joined >= timezone.now() - datetime.timedelta(days=settings.TOKEN_EXPIRY_DAYS)

    def save(self, **kwargs):
        self.user.save()
        super(Ureporter, self).save()

    def delete(self):
        self.user.delete()
        super(Ureporter, self).delete()

    def __unicode__(self):
        return self.uuid
