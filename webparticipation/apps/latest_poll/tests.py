from django.core import mail
from mock import Mock, patch, MagicMock
from django.test import TestCase, RequestFactory

from django.contrib.auth.models import User

from webparticipation.apps.latest_poll.decorators import show_untaken_latest_poll_message
from webparticipation.apps.latest_poll.tasks import retrieve_latest_poll, notify_users_of_new_poll
from webparticipation.apps.ureporter.models import Ureporter
from webparticipation.apps.latest_poll.models import LatestPoll


class TestLatestPoll(TestCase):
    def setUp(self):
        self.latest_poll_singleton = LatestPoll.get_solo()
        self.latest_poll_singleton.poll_id = 1
        self.latest_poll_singleton.save()

        self.latest_poll_id = 2
        self.should_receive_email_user = Ureporter.objects \
            .create(last_poll_taken=1, subscribed=True,
                    user=User.objects.create_user(username='remindme',
                                                  email='remindme@email.com'))
        self.already_taken_poll_user = Ureporter.objects \
            .create(last_poll_taken=2, subscribed=True,
                    user=User.objects.create_user(username='beenthere',
                                                  email='beenthere@email.com'))
        self.not_subscribed_user = Ureporter.objects \
            .create(last_poll_taken=2, subscribed=False,
                    user=User.objects.create_user(username='postnobills',
                                                  email='postnobills@email.com'))

    def tearDown(self):
        self.should_receive_email_user.delete()
        self.already_taken_poll_user.delete()
        self.not_subscribed_user.delete()
        self.latest_poll_singleton.delete()
        self.latest_poll_singleton.featured_polls = '0'
        self.latest_poll_singleton.save()

    def test_get_featured_polls_set_with_default(self):
        self.latest_poll_singleton.featured_polls = '0'
        self.assertFalse(self.latest_poll_singleton.has_in_previous_featured_polls(self.latest_poll_id))

    def test_get_featured_polls_set_with_same_poll_id(self):
        self.latest_poll_singleton.featured_polls = '0,1'
        featured_polls_set = self.latest_poll_singleton.get_featured_polls_set()
        self.assertEqual(featured_polls_set, set([0, 1]))

    def test_has_in_previous_featured_polls(self):
        self.latest_poll_singleton.featured_polls = '0,1,2'
        self.assertTrue(self.latest_poll_singleton.has_in_previous_featured_polls(1))
        self.assertFalse(self.latest_poll_singleton.has_in_previous_featured_polls(6))

    def test_add_featured_poll(self):
        self.latest_poll_singleton.featured_polls = '0,1,2'
        self.latest_poll_singleton.add_featured_poll(5)
        self.assertEqual(self.latest_poll_singleton.featured_polls, '0,1,2,5')

    @patch('requests.get')
    @patch('webparticipation.apps.latest_poll.tasks.notify_users_of_new_poll')
    def test_retrieve_latest_poll_when_latest_poll_not_updated(self, mock_notify_users_of_new_poll, mock_requests_get):
        mock_notify_users_of_new_poll.return_value = None
        mock_requests_get.return_value = mock_response = Mock()
        mock_response.json.return_value = {'results': [{'id': self.latest_poll_singleton.poll_id, 'flow_uuid': 'flow id'}]}
        retrieve_latest_poll()
        mock_notify_users_of_new_poll.assert_not_called()

    @patch('requests.get')
    @patch('webparticipation.apps.latest_poll.tasks.notify_users_of_new_poll')
    def test_retrieve_latest_poll_when_latest_poll_updated(self, mock_notify_users_of_new_poll, mock_requests_get):
        mock_notify_users_of_new_poll.return_value = None
        mock_requests_get.return_value = mock_response = Mock()
        mock_response.json.return_value = {'results': [{'id': self.latest_poll_id, 'flow_uuid': 'flow id'}]}
        retrieve_latest_poll()
        mock_notify_users_of_new_poll.assert_called_once_with(2)

    @patch('requests.get')
    def test_notify_users_of_new_poll(self, mock_requests_get):
        mock_requests_get.return_value = mock_response = Mock()
        mock_response.json.return_value = {'title': 'whatever'}
        notify_users_of_new_poll(self.latest_poll_id)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['remindme@email.com'])
        self.assertIn("profile/unsubscribe/%s" % self.should_receive_email_user.unsubscribe_token ,mail.outbox[0].body )


@show_untaken_latest_poll_message
def test_view(request):
    return request


class TestShowUnTakenPollMessage(TestCase):
    def setUp(self):
        self.latest_poll_singleton = LatestPoll.get_solo()
        self.latest_poll_singleton.poll_id = 1
        self.latest_poll_singleton.flow_uuid = "flow uuid"
        self.latest_poll_singleton.save()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='the user',
                                             email='beenthere@email.com')
        self.reporter = Ureporter.objects \
            .create(last_poll_taken=1, subscribed=True,
                    user=self.user)

    @patch('webparticipation.apps.latest_poll.decorators.complete_run_already_exists')
    def test_should_show_message_if_user_has_no_completed_latest_poll(self, mock_complete_run):
        mock_complete_run.return_value = False
        request = self.factory.get('/?lp=true')
        request.session = MagicMock()
        request.user = self.user
        response = test_view(request)
        self.assertEqual(True, response.session.lp)

    @patch('webparticipation.apps.latest_poll.decorators.complete_run_already_exists')
    def test_should_not_show_message_if_user_has_completed_latest_poll(self, mock_complete_run):
        mock_complete_run.return_value = True
        request = self.factory.get('/?lp=true')
        request.session = MagicMock()
        request.user = self.user
        response = test_view(request)
        self.assertEqual(False, response.session.lp)
