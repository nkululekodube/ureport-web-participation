from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from mock import patch
from webparticipation.apps.ureporter.models import Ureporter
from views import has_password_keyword, register, get_user
from webparticipation.apps.utils.views import undashify_user


class TestRegistration(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.uuid = 'octagons-help-feed-some-elephantsies'
        self.undashified_uuid = undashify_user(self.uuid)
        self.ureporter = Ureporter.objects.create(uuid=self.uuid, user=User.objects.create_user(username='registerMe'))

    def tearDown(self):
        self.ureporter.delete()

    # @patch('webparticipation.apps.register.views')
    # def test_get_register(self, mock_register):
    #     mock_get_user = create_autospec(get_user, return_value=self.ureporter)
    #     # mock_register.get_user.return_value = self.ureporter
    #     request = self.factory.get('/register/', {})
    #     mock_get_user(request)
    #     response = register(request)
    #     self.assertEqual(response.status_code, 200)
    #     mock_register.serve_get_response.assert_called_with(request, self.ureporter.uuid)

    # @patch('webparticipation.apps.register.views.get_already_registered_message')
    # def test_already_registered_user(self, mock_get_already_registered_message):
    #     request = self.factory.get('/register', {'phone': self.undashified_uuid, 'text': 'any@kinda.address'})
    #     mock_get_already_registered_message.assert_called_with(request)

    def test_registration_url_is_ok(self):
        response = self.client.get('/register/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'register.html')

    def test_has_password_keyword(self):
        messages = [{'msg_text': "lorem ipsum habeus borat"}]
        self.assertEqual(has_password_keyword(messages), False)
        messages = [{'msg_text': "A sentence containing password keyword"}]
        self.assertEqual(has_password_keyword(messages), True)
