from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from webparticipation.apps.ureporter.models import Ureporter
import json
from views import confirm_token


class TestConfirmToken(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.uuid = 'f3a12ae7-4f05-4fce-8135-bc51a9522116'
        self.undashified_uuid = 'f3a12ae74f054fce8135bc51a9522116'
        self.username = 'confirming-user'
        self.ureporter = Ureporter(uuid=self.uuid, user=User.objects.create_user(self.username))
        self.ureporter.token = 1234
        self.ureporter.save()

    def tearDown(self):
        self.ureporter.delete()

    def test_confirm_token_with_good_code(self):
        request = self.factory.post('/confirm-token', {'phone': self.undashified_uuid, 'text': '1234'})
        response = confirm_token(request)
        self.assertEqual(json.loads(response.content)['token_ok'], 'true')

    def test_confirm_token_with_bad_code(self):
        request = self.factory.post('/confirm-token', {'phone': self.undashified_uuid, 'text': '8888'})
        response = confirm_token(request)
        self.assertEqual(json.loads(response.content)['token_ok'], 'false')
