from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from webparticipation.apps.ureporter.models import Ureporter
from mock import patch
from views import poll_response


class TestPollResponse(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.uuid = 'cheetahs-flew-over-golf-sanctuariess'
        self.username = 'pollingGuy'
        self.password = 'password'
        self.ureporter = Ureporter.objects.create(
            uuid=self.uuid, user=User.objects.create_user(username=self.username, password=self.password))
        self.ureporter.save()

    def tearDown(self):
        self.ureporter.delete()

    @patch('webparticipation.apps.poll_response.views.serve_get_response')
    @patch('webparticipation.apps.poll_response.views.get_flow_info_from_poll_id')
    def test_poll_response(self, mock_get_flow_info_from_poll_id, mock_serve_get_response):
        self.client.login(username=self.username, password=self.password)
        mock_get_flow_info_from_poll_id.return_value = '18e85fe7-1aaf-473a-b0a1-505fe38d6717'
        request = self.factory.get('/poll/2/respond/')
        request.user = self.ureporter.user
        poll_response(request, 2)
        mock_serve_get_response.assert_called_once_with(
            request, 2, '18e85fe7-1aaf-473a-b0a1-505fe38d6717', self.username, self.uuid)
