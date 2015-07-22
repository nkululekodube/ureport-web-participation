from django.test import TestCase, Client
from mock import Mock, patch
from django.conf import settings
import requests


class TestRapidproReceptor(TestCase):

    def setUp(self):
        self.params = {
            'to': 'something',
            'from': 'someuser',
            'channel': 1,
            'id': 'someid',
            'text': 'sometext'
        }
        self.response = self.client.post('/rapidpro-receptor/', self.params)

    def test_receptor_is_available(self):
        self.assertEqual(200, self.response.status_code)

    def test_receptor_returns_confirmation_message(self):
        self.assertEqual('OK', self.response.content)

    @patch("requests.post")
    def test_receptor_makes_post_request(self, mocked_post_request):
        self.params = {
            'to': 'something',
            'from': 'someuser',
            'channel': 1,
            'id': 'someid',
            'text': 'sometext'
        }
        self.response = self.client.post('/rapidpro-receptor/', self.params)
        mocked_post_request.assert_called_with(
            settings.RAPIDPRO_RECEIVED_PATH,
            data={'from': self.params['to'], 'text': self.params['text']})
