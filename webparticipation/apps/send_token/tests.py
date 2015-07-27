from django.test import TestCase
from webparticipation.apps.ureport_user.models import UreportUser

class TestSendToken(TestCase):

    def setUp(self):
        self.uuid = 'f3a12ae7-4f05-4fce-8135-bc51a9522116'
        self.user = UreportUser.objects.create(uuid=self.uuid)
