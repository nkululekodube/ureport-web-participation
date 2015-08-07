from django.conf import settings
from django.db import models


class PasswordReset(models.Model):
    expiry = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    @staticmethod
    def build(expiry, user):
        return PasswordReset(expiry=expiry, user=user)

    def __unicode__(self):
        return self.user
