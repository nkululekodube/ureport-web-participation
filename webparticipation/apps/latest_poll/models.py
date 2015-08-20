from django.db import models

from solo.models import SingletonModel


class LatestPoll(SingletonModel):

    poll_id = models.IntegerField(null=True)
