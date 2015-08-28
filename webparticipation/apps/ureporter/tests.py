from mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory

from webparticipation.apps.utils.views import undashify_user
from webparticipation.apps.latest_poll.models import LatestPoll

from models import generate_token, Ureporter
from views import generate_random_urn_tel, get_user, save_new_ureporter


class UreporterTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.uuid = 'octagons-help-feed-some-elephantsies'
        self.undashified_uuid = undashify_user(self.uuid)
        self.ureporter = Ureporter.objects.create(uuid=self.uuid, user=User.objects.create_user(username='registerMe'))
        self.ureporter.save()

    @patch('requests.delete')
    def tearDown(self, mock_requests_delete):
        mock_requests_delete.side_effect = None
        self.ureporter.delete()

    def test_generate_token(self):
        token = generate_token()
        self.assertGreater(int(token), 999)
        self.assertLess(int(token), 10000)

    def test_invalidate_token(self):
        ureporter = Ureporter.objects.create(uuid='aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee',
                                             user=User.objects.create_user('invalidateMe'))
        self.assertNotEqual(ureporter.token, 0)
        ureporter.invalidate_token()
        self.assertEqual(ureporter.token, 0)

    def test_is_latest_poll_taken_for_new_user(self):
        self.assertFalse(self.ureporter.is_latest_poll_taken())

    def test_is_latest_poll_taken(self):
        LatestPoll.objects.create(poll_id=10)
        self.ureporter.last_poll_taken = 10
        self.ureporter.save()
        self.assertTrue(self.ureporter.is_latest_poll_taken())

    def test_set_uuid(self):
        ureporter = Ureporter.objects.create(uuid='aaaaaaaa-bbbb-cccc-dddd-000000000000',
                                             user=User.objects.create_user('changeMyUuid'))
        self.assertEqual(ureporter.uuid, 'aaaaaaaa-bbbb-cccc-dddd-000000000000')
        ureporter.set_uuid('aaaaaaaa-bbbb-cccc-dddd-111111111111')
        self.assertNotEqual(ureporter.uuid, 'aaaaaaaa-bbbb-cccc-dddd-000000000000')
        self.assertEqual(ureporter.uuid, 'aaaaaaaa-bbbb-cccc-dddd-111111111111')

    def test_save_user(self):
        ureporter = Ureporter.objects.create(uuid='aaaaaaaa-bbbb-cccc-dddd-yyyyyyyyyyyy',
                                             user=User.objects.create_user('saveMe'))
        self.assertEqual(User.objects.filter(email='save@this.email').exists(), False)
        self.assertEqual(Ureporter.objects.filter(token=5852).exists(), False)
        ureporter = Ureporter.objects.get(uuid='aaaaaaaa-bbbb-cccc-dddd-yyyyyyyyyyyy')
        ureporter.user.email = 'save@this.email'
        ureporter.token = 5852
        ureporter.save()
        self.assertEqual(User.objects.filter(email='save@this.email').exists(), True)
        self.assertEqual(Ureporter.objects.filter(token=5852).exists(), True)

    @patch('requests.delete')
    def test_delete_user(self, mock_requests_delete):
        mock_requests_delete.side_effect = None
        ureporter = Ureporter.objects.create(uuid='aaaaaaaa-bbbb-cccc-dddd-zzzzzzzzzzzz',
                                             user=User.objects.create_user('deleteMe'))
        self.assertEqual(User.objects.filter(username='deleteMe').exists(), True)
        self.assertEqual(Ureporter.objects.filter(uuid='aaaaaaaa-bbbb-cccc-dddd-zzzzzzzzzzzz').exists(), True)
        ureporter.delete()
        self.assertEqual(User.objects.filter(username='deleteMe').exists(), False)
        self.assertEqual(Ureporter.objects.filter(uuid='aaaaaaaa-bbbb-cccc-dddd-zzzzzzzzzzzz').exists(), False)

    def test_get_user_with_uuid(self):
        request = self.factory.post('/register/', {'uuid': self.uuid})
        ureporter = get_user(request)
        self.assertEqual(ureporter, self.ureporter)

    @patch('webparticipation.apps.ureporter.views.create_new_ureporter')
    def test_get_user_with_no_uuid(self, mock_create_new_ureporter):
        mock_create_new_ureporter.return_value = 'mock Ureport instance'
        request = self.factory.post('/register/', {})
        get_user(request)
        mock_create_new_ureporter.assert_called_once_with()

    def test_save_new_ureporter(self):
        uuid = 'referees-runs-foot-ball-oldtraffordd'
        urn_tel = 'user111111111'
        ureporter = save_new_ureporter(uuid, urn_tel)
        self.assertEqual(ureporter.uuid, uuid)
        self.assertEqual(ureporter.urn_tel, urn_tel)

    def test_generate_random_urn_tel(self):
        urn_tel = generate_random_urn_tel()
        self.assertRegexpMatches(urn_tel, r'user[0-9]{9}')
