from mock import patch

from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User

from webparticipation.apps.ureporter.models import Ureporter
from webparticipation.apps.utils.views import undashify_user
from webparticipation.apps.message_bus.models import MessageBus

from views import register, serve_get_response, has_password_keyword


class TestRegistration(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.uuid = 'octagons-help-feed-some-elephantsies'
        self.undashified_uuid = undashify_user(self.uuid)
        self.username = 'registerMe'
        self.ureporter = Ureporter.objects.create(uuid=self.uuid, user=User.objects.create_user(username=self.username))
        self.ureporter.save()

    def tearDown(self):
        self.ureporter.delete()
        MessageBus.objects.all().delete()

    @patch('webparticipation.apps.register.views.get_user')
    @patch('webparticipation.apps.register.views.serve_get_response')
    def test_register_with_get_method(self, mock_serve_get_response, mock_get_user):
        mock_get_user.return_value = self.ureporter
        request = self.factory.get('/register/')
        register(request)
        mock_serve_get_response.assert_called_once_with(request, self.uuid)

    @patch('webparticipation.apps.register.views.get_user')
    @patch('webparticipation.apps.register.views.serve_post_response')
    def test_register_with_post_method(self, mock_serve_post_response, mock_get_user):
        mock_get_user.return_value = self.ureporter
        request = self.factory.post('/register/')
        register(request)
        mock_serve_post_response.assert_called_once_with(request, self.uuid, self.ureporter)

    @patch('webparticipation.apps.register.views.get_already_registered_message')
    @patch('webparticipation.apps.register.views.user_is_authenticated')
    def test_serve_get_response_when_user_is_authenticated(
            self, mock_user_is_authenticated, mock_get_already_registered_message):
        mock_user_is_authenticated.return_value = True
        request = self.factory.post('/register/', {})
        serve_get_response(request, self.uuid)
        mock_get_already_registered_message.assert_called_once_with(request)

    def test_has_password_keyword(self):
        MessageBus.objects.create(msg_id=123, msg_channel=1, msg_to=self.username, msg_from='somechannel',
                                  msg_text='no pw keyword here')
        messages = MessageBus.objects.filter(msg_to=self.username)
        self.assertEqual(has_password_keyword(messages, self.username), False)

        MessageBus.objects.create(msg_id=123, msg_channel=1, msg_to=self.username, msg_from='somechannel',
                                  msg_text='A sentence containing password keyword')
        messages = MessageBus.objects.filter(msg_to=self.username)
        self.assertEqual(has_password_keyword(messages, self.username), True)
