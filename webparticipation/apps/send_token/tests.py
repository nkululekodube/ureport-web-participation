import json
from django.test import TestCase
from django.test.client import RequestFactory
from mock import patch
from django.contrib.auth.models import User
from webparticipation.apps.ureporter.models import Ureporter
from webparticipation.apps.utils.views import undashify_user
from views import send_token
from tasks import send_verification_token


class TestSendToken(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.uuid = 'f3a12ae7-4f05-4fce-8135-bc51a9522116'
        self.undashified_uuid = undashify_user(self.uuid)
        self.ureporter = Ureporter.objects.create(uuid=self.uuid, user=User.objects.create_user('username'))
        self.username = self.ureporter.urn_tel
        self.ureporter.user.email = 'an@existing.user'
        self.ureporter.save()

    @patch('requests.delete')
    def tearDown(self, mock_requests_delete):
        mock_requests_delete.side_effect = None
        self.ureporter.delete()

    @patch('webparticipation.apps.send_token.tasks.send_verification_token.delay')
    def test_send_token_does_not_accept_get(self, mock_send_verification_token):
        mock_send_verification_token.return_value = None
        request = self.factory.get('/send-token', {'phone': self.undashified_uuid, 'text': 'any@kinda.address'})
        response = send_token(request)
        self.assertEqual(response, None)

    @patch('webparticipation.apps.send_token.tasks.send_verification_token.delay')
    def test_send_token_to_new_user(self, mock_send_verification_token):
        mock_send_verification_token.return_value = None
        request = self.factory.post('/send-token', {'phone': self.username, 'text': 'an@ok.address'})
        response = send_token(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['send_token'], 'send')

    @patch('requests.delete')
    @patch('webparticipation.apps.send_token.tasks.send_verification_token.delay')
    def test_send_token_to_user_that_has_not_finished_registration(
            self, mock_send_verification_token, mock_requests_delete):
        mock_send_verification_token.return_value = None
        mock_requests_delete.side_effect = None
        request = self.factory.post('/send-token', {'phone': self.username, 'text': 'an@existing.user'})
        response = send_token(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['send_token'], 'send')

    @patch('requests.delete')
    @patch('webparticipation.apps.send_token.tasks.send_verification_token.delay')
    def test_do_not_send_token_to_existing_user(self, mock_send_verification_token, mock_requests_delete):
        mock_send_verification_token.return_value = None
        mock_requests_delete.side_effect = None
        self.ureporter.token = 0
        self.ureporter.save()
        request = self.factory.post('/send-token', {'phone': self.username, 'text': 'an@existing.user'})
        response = send_token(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['send_token'], 'exists')

    @patch('django.core.mail.EmailMessage.send')
    def test_task_send_verification_message_sent(self, mock_email_send):
        send_verification_token(self.ureporter)
        mock_email_send.assert_called_with()
