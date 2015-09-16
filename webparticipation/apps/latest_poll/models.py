from django.db import models

from solo.models import SingletonModel


class LatestPoll(SingletonModel):

    poll_id = models.IntegerField(null=True)
    featured_polls = models.CommaSeparatedIntegerField(max_length=4096, default='0')

    def set_poll_id(self, poll_id):
        self.poll_id = poll_id
        self.save()

    def get_featured_polls_set(self):
        featured_polls_set = set([int(item) for item in self.featured_polls.split(',')])
        return featured_polls_set

    def has_in_previous_featured_polls(self, poll_id):
        return poll_id in self.get_featured_polls_set()

    def add_featured_poll(self, poll_id):
        self.featured_polls = '%s,%s' % (self.featured_polls, str(poll_id))
        self.save()
