from django.test import TestCase
from webparticipation.apps.ureporter.models import Ureporter
from django.test.client import RequestFactory
from webparticipation.apps.ureporter.models import Ureporter
from views import get_uuid, send_token
import json


class TestSendToken(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.uuid = 'f3a12ae7-4f05-4fce-8135-bc51a9522116'
        self.undashified_uuid = 'f3a12ae74f054fce8135bc51a9522116'
        self.user = Ureporter.objects.create(uuid=self.uuid)

    def test_send_token(self):
        request = self.factory.post('/send-token', {'phone': self.undashified_uuid, 'text': 'an@ok.address'})
        response = send_token(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['send_token'], 'send')

    def test_get_uuid(self):
        request = self.factory.post('/send-token', {'phone': self.undashified_uuid, 'text': 'whatever'})
        uuid = get_uuid(request)
        self.assertEqual(self.uuid, uuid)
