from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import TestCase, RequestFactory, Client
from mock import patch

from webparticipation.apps.ureport_auth.tasks import send_forgot_password_email
from webparticipation.apps.ureport_auth.views import login_user
from webparticipation.apps.ureporter.models import Ureporter


class TestUserLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_login_url(self):
        response = self.client.get('/login/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'login.html')

    def test_forgot_password_url(self):
        response = self.client.get('/forgot-password/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'forgot_password.html')

    def test_user_is_logged_in(self):
        ureporter = Ureporter.objects.create(
            user=User.objects.create_user(username='jacob', email='john@doe.com', password='top_secret'))
        request = self.factory.post('/login', {'email': ureporter.user.email, 'password': 'top_secret'})
        session = self.client.session
        request.session = session
        messages = FallbackStorage(request)
        request._messages = messages
        request.user = ureporter.user.username
        response = login_user(request)
        self.assertEqual(response.status_code, 302)

    def test_invalid_user_login_details(self):
        request = self.factory.post('/login', {'email': 'non@existent.guy', 'password': 'top_secret'})
        session = self.client.session
        setattr(request, 'session', session)
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = None
        response = login_user(request)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('There is no registered user with '
                        'sign-in email' in response.content)

    def test_unregistered_user_cannot_reset_password(self):
        response = self.client.post('/forgot-password/', {'email': 'unregistered@email.com'})
        self.assertEqual(response.templates[0].name, 'forgot_password.html')
        self.assertTrue('There is no registered user with '
                        'sign-in email' in response.content)

    @patch('django.core.mail.EmailMessage.send')
    def test_task_password_reset_message_sent(self, mock_email_send):
        ureporter = Ureporter.objects.create(uuid='aaaaaaaa-bbbb-cccc-dddd-zzzzzzzzzzzz',
                                             user=User.objects.create_user('user'))
        ureporter.user.email = 'user@email.com'
        ureporter.user.save()
        send_forgot_password_email(ureporter.user.email)
        mock_email_send.assert_called_with()
