from django.test import TestCase
from mock import patch

from webparticipation.apps.message_bus.models import MessageBus
from webparticipation.apps.rapidpro_receptor.views import get_filtered_messages, remove_messages_from_message_bus, \
    get_sorted_message_ids


class TestRapidproReceptor(TestCase):

    def setUp(self):
        self.params = {'to': 'someone', 'from': 'someuser', 'channel': 1, 'id': 123, 'text': 'sometext'}
        self.message1_pt1 = {'to': 'user123456', 'from': 'rapidpro', 'channel': 1, 'id': 200,
                             'text': 'Hey there!'}
        self.message1_pt2 = {'to': 'user123456', 'from': 'rapidpro', 'channel': 1, 'id': 200,
                             'text': 'So you wanna join ureport eh?'}
        self.message2 = {'to': 'user123456', 'from': 'rapidpro', 'channel': 1, 'id': 201,
                         'text': 'What is your email address?'}
        MessageBus.objects.create(
            msg_id=self.message1_pt2['id'],
            msg_channel=self.message1_pt2['channel'],
            msg_to=self.message1_pt2['to'],
            msg_from=self.message1_pt2['from'],
            msg_text=self.message1_pt2['text'])
        MessageBus.objects.create(
            msg_id=self.message1_pt1['id'],
            msg_channel=self.message1_pt1['channel'],
            msg_to=self.message1_pt1['to'],
            msg_from=self.message1_pt1['from'],
            msg_text=self.message1_pt1['text'])
        MessageBus.objects.create(
            msg_id=self.message2['id'],
            msg_channel=self.message2['channel'],
            msg_to=self.message2['to'],
            msg_from=self.message2['from'],
            msg_text=self.message2['text'])

    def tearDown(self):
        MessageBus.objects.filter(msg_to='user123456').delete()

    @patch('apps.rapidpro_receptor.views.send_message_to_rapidpro')
    def test_receptor_is_available(self, mock_post):
        mock_post.return_value = None
        self.response = self.client.post('/rapidpro-receptor', self.params)
        self.assertEqual(200, self.response.status_code)

    @patch('apps.rapidpro_receptor.views.send_message_to_rapidpro')
    def test_receptor_returns_confirmation_message(self, mock_post):
        mock_post.return_value = None
        self.response = self.client.post('/rapidpro-receptor', self.params)
        self.assertEqual('OK', self.response.content)

    def test_get_filtered_messages(self):
        filtered_messages = get_filtered_messages('user123456')
        self.assertEqual(len(filtered_messages), 3)

    def test_remove_messages_from_message_bus(self):
        remove_messages_from_message_bus('user123456')
        self.assertEqual(MessageBus.objects.filter(msg_to='user123456').exists(), False)

    def test_get_sorted_message_ids(self):
        sorted_message_ids = get_sorted_message_ids('user123456')
        self.assertEqual(len(sorted_message_ids), 2)
        self.assertEqual(sorted_message_ids[0], 200)
        self.assertEqual(sorted_message_ids[1], 201)
