from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from mock import patch
from webparticipation.apps.ureporter.models import Ureporter
from views import has_password_keyword, register, get_user, save_new_ureporter, \
    generate_random_urn_tel, serve_get_response, get_already_registered_message
from webparticipation.apps.utils.views import undashify_user
# import responses
# import requests
# import os


class TestRegistration(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.uuid = 'octagons-help-feed-some-elephantsies'
        self.undashified_uuid = undashify_user(self.uuid)
        self.ureporter = Ureporter.objects.create(uuid=self.uuid, user=User.objects.create_user(username='registerMe'))
        self.ureporter.save()

    def tearDown(self):
        self.ureporter.delete()

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

    def test_get_user_with_uuid(self):
        request = self.factory.post('/register/', {'uuid': self.uuid})
        ureporter = get_user(request)
        self.assertEqual(ureporter, self.ureporter)

    @patch('webparticipation.apps.register.views.create_new_ureporter')
    def test_get_user_with_no_uuid(self, mock_create_new_ureporter):
        mock_create_new_ureporter.return_value = 'mock Ureport instance'
        request = self.factory.post('/register/', {})
        get_user(request)
        mock_create_new_ureporter.assert_called_once_with()

    def test_create_new_ureporter(self):
        pass

    def test_create_new_rapidpro_contact(self):
        pass

    def test_save_new_ureporter(self):
        uuid = 'referees-runs-foot-ball-oldtraffordd'
        urn_tel = 'user111111111'
        ureporter = save_new_ureporter(uuid, urn_tel)
        self.assertEqual(ureporter.uuid, uuid)
        self.assertEqual(ureporter.urn_tel, urn_tel)

    def test_generate_random_urn_tel(self):
        urn_tel = generate_random_urn_tel()
        self.assertRegexpMatches(urn_tel, r'user[0-9]{9}')

    @patch('webparticipation.apps.register.views.get_already_registered_message')
    @patch('webparticipation.apps.register.views.user_is_authenticated')
    def test_serve_get_response_when_user_is_authenticated(
            self, mock_user_is_authenticated, mock_get_already_registered_message):
        mock_user_is_authenticated.return_value = True
        request = self.factory.post('/register/', {})
        serve_get_response(request, self.uuid)
        mock_get_already_registered_message.assert_called_once_with(request)

    # @patch('django.shortcuts.render')
    # @patch('webparticipation.apps.register.views.get_messages_for_user')
    # @patch('webparticipation.apps.utils.views.send_message_to_rapidpro')
    # @patch('webparticipation.apps.register.views.user_is_authenticated')
    # def test_serve_get_response_when_user_is_not_authenticated(
    #         self, mock_user_is_authenticated, mock_send_message_to_rapidpro, mock_get_messages_for_user, mock_render):
    #     mock_user_is_authenticated.return_value = False
    #     mock_send_message_to_rapidpro.return_value = None
    #     mock_get_messages_for_user.return_value = {'messages': [{'msg_text': "some message"}]}
    #     request = self.factory.post('/register/', {})
    #     serve_get_response(request, self.uuid)
    #     mock_render.assert_called_once_with(
    #         request,
    #         'register.html',
    #         {'messages': {'messages': [{'msg_text': "some message"}]}, 'uuid': self.uuid})

    # @patch('django.shortcuts.render')
    # def test_get_already_registered_message(self, mock_render):
    #     print mock_render
    #     request = self.factory.post('/register/', {})
    #     response = get_already_registered_message(request)
    #     mock_render.assert_called_once_with(
    #         request,
    #         'register.html',
    #         {'messages': [{'msg_text': "You're already logged in. Why don't you take our latest poll?"}]})
    #     self.assertEqual(response.status_code, 200)

    def test_has_password_keyword(self):
        messages = [{'msg_text': "lorem ipsum habeus borat"}]
        self.assertEqual(has_password_keyword(messages), False)
        messages = [{'msg_text': "A sentence containing password keyword"}]
        self.assertEqual(has_password_keyword(messages), True)
