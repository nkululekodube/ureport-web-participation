from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from webparticipation.apps.ureporter.models import Ureporter
from views import home
from mock import patch


class TestHome(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.uuid = 'octagons-help-feed-some-elephantsies'
        self.username = 'homepage'
        self.ureporter = Ureporter.objects.create(uuid=self.uuid, user=User.objects.create_user(username=self.username))
        self.ureporter.save()

    def tearDown(self):
        self.ureporter.delete()

    def test_home(self):
        request = self.factory.get('/')
        request.user = self.username
        response = home(request)
        self.assertEqual(response.status_code, 200)
