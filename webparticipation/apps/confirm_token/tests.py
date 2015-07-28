from django.test import TestCase
from django.http import HttpResponse, QueryDict
from webparticipation.apps.ureporter.models import Ureporter
import requests
from . import views

class TestConfirmToken(TestCase):

    def setUp(self):
        self.user = Ureporter.objects.create(uuid='f3a12ae7-4f05-4fce-8135-bc51a9522116')


    def test_confirm_token_with_good_code(self):
        pass
        # post_params = QueryDict('phone=f3a12ae74f054fce8135bc51a9522116&text=' + str(self.user.token))
        # self.params = {
        #     'POST': post_params
        # }
        # self.response = self.client.post('/confirm-token', self.params)
        # self.assertEqual(200, self.response.status_code)
        # self.assertEqual({'status': 200}, self.response)
