from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase, RequestFactory
from mock import patch
from webparticipation.apps.ureport_auth.tasks import send_forgot_password_email
from webparticipation.apps.ureport_auth.views import login_user, forgot_password
from django.contrib.messages.storage.fallback import FallbackStorage
from webparticipation.apps.ureporter.models import Ureporter


class TestUserLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_login_url_is_ok(self):
        response = self.client.get('/login/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'login.html')

    def test_user_is_logged_in(self):
        user = User.objects.create_user(username='jacob', email='john@doe.com', password='top_secret')
        user.save()
        request = self.factory.post('/login', {'email': user.email, 'password': 'top_secret'})

        session = self.client.session
        setattr(request, 'session', session)
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = login_user(request)
        self.assertEqual(response.status_code, 302)

    def test_invalid_user_details(self):
        request = self.factory.post('/login', {'email': 'non@existent.guy', 'password': 'top_secret'})

        session = self.client.session
        setattr(request, 'session', session)
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = login_user(request)
        self.assertEquals(response.status_code, 200)

    def test_forgot_password_url_is_ok(self):
        response = self.client.get('/forgot-password/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'forgot_password.html')

    def test_forgot_password_redirects_to_password_reset(self):
        user = User.objects.create_user(username='jane', email='jane@murdoch.com', password='top_secret')
        user.save()
        request = self.factory.post('/forgot-password', {'email': user.email})
        session = self.client.session
        setattr(request, 'session', session)
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = forgot_password(request)
        self.assertEqual(response.status_code, 200)

    @patch('django.core.mail.EmailMessage.send')
    def test_task_password_reset_message_sent(self, mock_email_send):
        ureporter = Ureporter.objects.create(uuid='aaaaaaaa-bbbb-cccc-dddd-zzzzzzzzzzzz',
                                             user=User.objects.create_user('user'))
        ureporter.user.email = 'user@email.com'
        ureporter.user.save()

        send_forgot_password_email(ureporter.user.email)
        mock_email_send.assert_called_with()