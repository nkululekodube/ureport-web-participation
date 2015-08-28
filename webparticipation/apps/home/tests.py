from mock import patch

from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User

from webparticipation.apps.ureporter.models import Ureporter

from views import home


class TestHome(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.uuid = 'octagons-help-feed-some-elephantsies'
        self.username = 'homepage'
        self.ureporter = Ureporter.objects.create(uuid=self.uuid, user=User.objects.create_user(username=self.username))
        self.ureporter.save()

    @patch('requests.delete')
    def tearDown(self, mock_requests_delete):
        mock_requests_delete.side_effect = None
        self.ureporter.delete()

    def test_home(self):
        request = self.factory.get('/')
        request.user = self.username
        response = home(request)
        self.assertEqual(response.status_code, 200)
