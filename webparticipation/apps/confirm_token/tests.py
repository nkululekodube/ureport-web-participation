from django.test import TestCase
from webparticipation.apps.ureporter.models import Ureporter
from django.contrib.auth.models import User


class TestConfirmToken(TestCase):

    def setUp(self):
        self.user = Ureporter(uuid='f3a12ae7-4f05-4fce-8135-bc51a9522116',
                              user=User.objects.create_user('someusername'))

    def test_confirm_token_with_good_code(self):
        pass
