from django.test import TestCase
from webparticipation.apps.ureporter.models import Ureporter
from django.contrib.auth.models import User


class TestProfilePage(TestCase):

    def setUp(self):
        self.ureporter = Ureporter.objects.create(uuid='aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee',
                                                  user=User.objects.create_user(username='legituser',
                                                                                password='password'))

        self.another_ureporter = Ureporter.objects.create(uuid='ffffffff-gggg-hhhh-iiii-jjjjjjjjjjjj',
                                                          user=User.objects.create_user(username='the_other_guy',
                                                                                        password='anotherpw'))

    def tearDown(self):
        self.client.logout()

    def test_anon_user_cannot_view_page(self):
        response = self.client.get('/profile/')
        self.assertIn('/login/?next=/profile/', response.url)
        self.assertEqual(response.status_code, 302)

    def test_user_can_view_profile(self):
        self.client.login(username='legituser', password='password')
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)

    def test_user_can_unsubscribe(self):
        self.assertEqual(self.ureporter.subscribed, True)
        self.client.login(username='legituser', password='password')
        response = self.client.post('/profile/unsubscribe/', {'subscribed': None})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ureporter.objects.get(uuid='aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee').subscribed, False)
