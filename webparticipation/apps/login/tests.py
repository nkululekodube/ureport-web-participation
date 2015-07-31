from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase, RequestFactory
from webparticipation.apps.login.views import login_user
from django.contrib.messages.storage.fallback import FallbackStorage


class TestUserLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_login_url_is_ok(self):
        response = self.client.get('/login/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'login.html')

    def test_user_is_logged_in(self):
        user = User.objects.create_user(username='jacob', email='jacob@email.com', password='top_secret')
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
