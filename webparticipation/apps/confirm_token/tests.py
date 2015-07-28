from django.test import TestCase
from django.http import HttpResponse, QueryDict
from webparticipation.apps.ureporter.models import Ureporter
import requests
from . import views
from django.test.client import RequestFactory


class TestConfirmToken(TestCase):

    def setUp(self):
        self.user = Ureporter.objects.create(uuid='f3a12ae7-4f05-4fce-8135-bc51a9522116')

    def test_confirm_token_with_good_code(self):
        pass
