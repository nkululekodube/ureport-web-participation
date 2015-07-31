import json
from django.test import TestCase
from django.test.client import RequestFactory
from mock import patch
from django.contrib.auth.models import User
from webparticipation.apps.ureporter.models import Ureporter
from webparticipation.apps.utils.views import undashify_user
from views import get_uuid, send_token
from tasks import send_verification_token


class TestSendToken(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.uuid = 'f3a12ae7-4f05-4fce-8135-bc51a9522116'
        self.undashified_uuid = undashify_user(self.uuid)
        self.ureporter = Ureporter.objects.create(uuid=self.uuid, user=User.objects.create_user('username'))
        self.ureporter.user.email = 'an@existing.user'
        self.ureporter.user.save()
        self.ureporter.save()

    def tearDown(self):
        self.ureporter.user.delete()
        self.ureporter.delete()

    def test_send_token_does_not_accept_get(self):
        request = self.factory.get('/send-token', {'phone': self.undashified_uuid, 'text': 'any@kinda.address'})
        response = send_token(request)
        self.assertEqual(response, None)

    def test_send_token_to_new_user(self):
        request = self.factory.post('/send-token', {'phone': self.undashified_uuid, 'text': 'an@ok.address'})
        response = send_token(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['send_token'], 'send')

    def test_send_token_to_user_that_has_not_finished_registration(self):
        request = self.factory.post('/send-token', {'phone': self.undashified_uuid, 'text': 'an@existing.user'})
        response = send_token(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['send_token'], 'send')

    def test_do_not_send_token_to_existing_user(self):
        self.ureporter.token = 0
        self.ureporter.save()
        request = self.factory.post('/send-token', {'phone': self.undashified_uuid, 'text': 'an@existing.user'})
        response = send_token(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['send_token'], 'exists')

    def test_get_uuid(self):
        request = self.factory.post('/send-token', {'phone': self.undashified_uuid, 'text': 'whatever'})
        uuid = get_uuid(request)
        self.assertEqual(self.uuid, uuid)

    # @patch('django.core.mail.EmailMessage')
    # def test_task_send_verification_email_constructed(self, mock_email_message_class):
    #     send_verification_token(self.ureporter)
    #     # instance = mock_email_message_class.return_value
    #     mock_email_message_class.assert_called_with('Hello', 'something with token', to=[self.ureporter.user.email])

    @patch('django.core.mail.EmailMessage.send')
    def test_task_send_verification_message_sent(self, mock_email_send):
        send_verification_token(self.ureporter)
        mock_email_send.assert_called_with()
