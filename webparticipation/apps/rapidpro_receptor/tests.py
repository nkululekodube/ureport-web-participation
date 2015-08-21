from django.test import TestCase
from mock import patch


class TestRapidproReceptor(TestCase):

    def setUp(self):
        self.params = {
            'to': 'someone',
            'from': 'someuser',
            'channel': 1,
            'id': 123,
            'text': 'sometext'
        }

    @patch('apps.rapidpro_receptor.views.send_message_to_rapidpro')
    def test_receptor_is_available(self, mock_post):
        mock_post.return_value = None
        self.response = self.client.post('/rapidpro-receptor', self.params)
        self.assertEqual(200, self.response.status_code)

    @patch('apps.rapidpro_receptor.views.send_message_to_rapidpro')
    def test_receptor_returns_confirmation_message(self, mock_post):
        mock_post.return_value = None
        self.response = self.client.post('/rapidpro-receptor', self.params)
        self.assertEqual('OK', self.response.content)
