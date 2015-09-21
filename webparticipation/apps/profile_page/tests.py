from django.test import TestCase
from webparticipation.apps.ureporter.models import Ureporter
from django.contrib.auth.models import User


class TestProfilePage(TestCase):

    def setUp(self):
        self.ureporter = Ureporter.objects.create(
            uuid='aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee',
            user=User.objects.create_user(username='legituser', password='password'))

    def tearDown(self):
        self.client.logout()
        self.ureporter.delete()

    def test_anon_user_cannot_view_page(self):
        response = self.client.get('/profile/')
        self.assertIn('/login/?next=/profile/', response.url)
        self.assertEqual(response.status_code, 302)

    def test_user_can_view_profile(self):
        self.client.login(username='legituser', password='password')
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)

    def test_user_can_unsubscribe(self):
        unsubscribe_token = self.ureporter.unsubscribe_token
        self.assertEqual(self.ureporter.subscribed, True)
        self.client.login(username='legituser', password='password')
        response = self.client.get('/profile/unsubscribe/%s/' % unsubscribe_token)
        self.ureporter = Ureporter.objects.get(uuid=self.ureporter.uuid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.ureporter.subscribed, False)
