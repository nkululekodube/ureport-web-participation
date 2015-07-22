from django.test import TestCase
from mock import patch
from django.core.mail import EmailMessage
from webparticipation.apps.ureport_user.models import UreportUser
from tasks import get_auth_token


class TestSendToken(TestCase):

    def setUp(self):
        self.uuid = 'f3a12ae7-4f05-4fce-8135-bc51a9522116'
        self.user = UreportUser.objects.create(uuid=self.uuid)

    def test_get_auth_token(self):
        token = get_auth_token(self.uuid)
        self.assertEqual(str(token), self.user.token)

    # @patch("EmailMessage.send")
    # def test_send_verification_token(self, mock_email_send):
    #     mock_email_send.assert_called_with()
