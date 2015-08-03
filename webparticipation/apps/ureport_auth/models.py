from django.conf import settings
from django.utils import timezone
from django.db import models


class PasswordReset(models.Model):
    expiry = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def is_valid(self):
        present = timezone.now()
        return self.expiry > present

    @staticmethod
    def build(expiry, user):
        return PasswordReset(expiry=expiry, user=user)

    @staticmethod
    def find(uuid):
        return PasswordReset.objects.get(uuid=uuid)

    def __unicode__(self):
        return self.user
