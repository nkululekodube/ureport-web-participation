from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase, RequestFactory
from webparticipation.apps.login.views import login_user


class TestUserLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_login_url_is_ok(self):
        response = self.client.get('/login/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'auth.html')

    def test_invalid_login_details(self):
        self.user = User.objects.create_user(
            username='jacob', email='jacob@email.com', password='top_secret')
        self.user.save()
        response = self.client.post('/login/')
        self.assertEquals(response.context['message'], 'User not registered.')
        self.assertEqual(response.status_code, 200)

    def test_user_is_logged_in(self):
        user = User.objects.create_user(
            username='jacob', email='jacob@email.com', password='top_secret')
        request = self.factory.get('/login')
        request.user = user
        response = login_user(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('location'), '/home')

    def test_user_is_logged_out(self):
        user = User.objects.create_user(username='jacob', email='jacob@email.com', password='top_secret')
        request = self.factory.get('/login')
        request.user = user
        response = login_user(request)
        self.assertEqual(200, response.status_code)
        response = logout(request)
        self.assertTemplateUsed(response, 'base.html')
        self.assertEqual(response.status_code, 200)
