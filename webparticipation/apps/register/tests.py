from django.conf import settings as s
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory
from mock import patch

from webparticipation.apps.message_bus.models import MessageBus
from webparticipation.apps.register.views import register, serve_get_response, has_password_keyword, \
    get_post_password_status
from webparticipation.apps.ureporter.models import Ureporter
from webparticipation.apps.utils.views import undashify_user


class TestRegistration(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.uuid = 'octagons-help-feed-some-elephantsies'
        self.urn_tel = 'user123456789'
        self.undashified_uuid = undashify_user(self.uuid)
        self.username = 'registerMe'
        self.ureporter = Ureporter.objects.create(
            uuid=self.uuid, user=User.objects.create_user(username=self.username), urn_tel=self.urn_tel)
        self.ureporter.save()

    @patch('requests.delete')
    def tearDown(self, mock_requests_delete):
        mock_requests_delete.side_effect = None
        self.ureporter.delete()
        MessageBus.objects.all().delete()

    @patch('webparticipation.apps.register.views.get_user')
    @patch('webparticipation.apps.register.views.serve_get_response')
    def test_register_with_get_method(self, mock_serve_get_response, mock_get_user):
        mock_get_user.return_value = self.ureporter
        request = self.factory.get('/register/')
        register(request)
        mock_serve_get_response.assert_called_once_with(request, self.ureporter)

    @patch('webparticipation.apps.register.views.get_already_logged_in_message')
    @patch('webparticipation.apps.register.views.user_is_authenticated')
    def test_serve_get_response_when_user_is_authenticated(
        self, mock_user_is_authenticated, mock_get_already_logged_in_message):
        mock_user_is_authenticated.return_value = True
        request = self.factory.get('/register/', {})
        serve_get_response(request, self.ureporter)
        mock_get_already_logged_in_message.assert_called_once_with(request)

    @patch('webparticipation.apps.register.views.get_user')
    @patch('webparticipation.apps.register.views.serve_post_response')
    def test_register_with_post_method(self, mock_serve_post_response, mock_get_user):
        mock_get_user.return_value = self.ureporter
        request = self.factory.post('/register/')
        register(request)
        mock_serve_post_response.assert_called_once_with(request, self.ureporter)

    @patch('webparticipation.apps.register.views.get_messages_for_user')
    @patch('webparticipation.apps.register.views.get_run_id')
    @patch('webparticipation.apps.register.views.render')
    @patch('webparticipation.apps.register.views.send_message_to_rapidpro')
    @patch('webparticipation.apps.register.views.user_is_authenticated')
    def test_serve_get_response_when_user_is_not_authenticated(
        self, mock_user_is_authenticated, mock_send_message_to_rapidpro, mock_render, mock_get_run_id,
        mock_get_messages_for_user):
        mock_user_is_authenticated.return_value = False
        mock_get_run_id.return_value = 123
        mock_get_messages_for_user.return_value = ['whatever'], True
        request = self.factory.get('/register/', {})
        serve_get_response(request, self.ureporter)
        mock_send_message_to_rapidpro.assert_called_once_with(
            {'from': self.urn_tel, 'text': s.RAPIDPRO_REGISTER_TRIGGER})
        mock_render.assert_called_once_with(
            request, 'register.html', {'messages': ['whatever'], 'uuid': self.uuid, 'run_id': 123})

    def test_has_password_keyword(self):
        MessageBus.objects.create(msg_id=123, msg_channel=1, msg_to=self.username, msg_from='somechannel',
                                  msg_text='no pw keyword here')
        messages = [msg.msg_text for msg in MessageBus.objects.filter(msg_to=self.username)]
        self.assertEqual(has_password_keyword(messages, self.username), False)

        MessageBus.objects.create(msg_id=123, msg_channel=1, msg_to=self.username, msg_from='somechannel',
                                  msg_text='A sentence containing password keyword')
        messages = [msg.msg_text for msg in MessageBus.objects.filter(msg_to=self.username)]
        self.assertEqual(has_password_keyword(messages, self.username), True)

    def test_show_latest_poll_link(self):
        request = self.factory.post('/register/', {'post_password': 0})
        post_password_status = get_post_password_status(request, False)
        self.assertEqual(int(post_password_status), 0)

        request = self.factory.post('/register/', {'post_password': 1})
        post_password_status = get_post_password_status(request, True)
        self.assertEqual(int(post_password_status), 1)

        request = self.factory.post('/register/', {'post_password': 1})
        post_password_status = get_post_password_status(request, False)
        self.assertEqual(int(post_password_status), 2)
