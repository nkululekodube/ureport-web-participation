from django.db import models


class MessageBus(models.Model):

    msg_id = models.PositiveIntegerField()
    msg_channel = models.PositiveIntegerField()
    msg_to = models.CharField(max_length=13, default=None)
    msg_from = models.CharField(max_length=64, default=None)
    msg_text = models.CharField(max_length=160, default=None)
