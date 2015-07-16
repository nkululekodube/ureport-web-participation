from django.test import TestCase, Client
from mock import Mock, patch
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
            'http://localhost:8000/api/v1/external/received/7a795bef-8c13-476e-9350-8799da09d362/',
            data={'from': self.params['to'], 'text': self.params['text']})

