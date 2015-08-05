from django.test import TestCase
from mock import patch
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

    @patch('apps.rapidpro_receptor.views.send_received_confirmation_to_rapidpro')
    def test_receptor_is_available(self, mock_post):
        mock_post.return_value = None
        self.response = self.client.post('/rapidpro-receptor', self.params)
        self.assertEqual(200, self.response.status_code)

    @patch('apps.rapidpro_receptor.views.send_received_confirmation_to_rapidpro')
    def test_receptor_returns_confirmation_message(self, mock_post):
        mock_post.return_value = None
        self.response = self.client.post('/rapidpro-receptor', self.params)
        self.assertEqual('OK', self.response.content)

    @patch('requests.post')
    def test_receptor_makes_rapidpro_post_request(self, mock_request_post):
        self.response = self.client.post('/rapidpro-receptor', self.params)
        mock_request_post.assert_called_with(
            os.environ.get('RAPIDPRO_RECEIVED_PATH'),
            data={'from': self.params['from'], 'text': self.params['text']})

    # @patch("settings.common.RAPIDPRO_DISPATCHER")
    # def test_receptor_makes_post_request(self, mock_dispatcher):
    #     self.response = self.client.post('/rapidpro-receptor', self.params)
    #     mock_dispatcher.send = lambda x: x
    #     mock_dispatcher.assert_called_with(
    #         sender=self.params['to'],
    #         param_id=self.params['id'],
    #         param_channel=self.params['channel'],
    #         param_from=self.params['from'],
    #         param_to=self.params['to'],
    #         param_text=self.params['text'])
