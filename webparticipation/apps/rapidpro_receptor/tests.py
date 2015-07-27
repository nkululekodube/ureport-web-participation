from django.test import TestCase
from mock import patch
from django.conf import settings
import os

class TestRapidproReceptor(TestCase):

    def setUp(self):
        self.params = {
            'to': 'someone',
            'from': 'someuser',
            'channel': 1,
            'id': 'someid',
            'text': 'sometext'
        }

    def test_receptor_is_available(self):
        self.response = self.client.post('/rapidpro-receptor', self.params)
        self.assertEqual(200, self.response.status_code)

    def test_receptor_returns_confirmation_message(self):
        self.response = self.client.post('/rapidpro-receptor', self.params)
        self.assertEqual('OK', self.response.content)

    @patch("requests.post")
    def test_receptor_makes_post_request(self, mocked_post_request):
        self.response = self.client.post('/rapidpro-receptor', self.params)
        mocked_post_request.assert_called_with(
            os.environ.get('RAPIDPRO_RECEIVED_PATH'),
            data={'from': self.params['from'], 'text': self.params['text']})
