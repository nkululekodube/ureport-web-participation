from django.test import TestCase
from webparticipation.apps.ureporter.models import Ureporter
from django.contrib.auth.models import User


class TestProfilePage(TestCase):

    def setUp(self):
        self.user = Ureporter.objects.create(uuid='aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee',
                                             user=User.objects.create_user(username='legituser', password='password'))
        self.user.save()

        self.another_user = Ureporter.objects.create(uuid='ffffffff-gggg-hhhh-iiii-jjjjjjjjjjjj',
                                                     user=User.objects.create_user(username='the_other_guy',
                                                                                   password='anotherpw'))
        self.another_user.save()

    def tearDown(self):
        self.client.logout()

    def test_anon_user_cannot_view_page(self):
        response = self.client.get('/ureporter/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee/')
        self.assertIn('/login/?next=/ureporter/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee/', response.url)
        self.assertEqual(response.status_code, 302)

    def test_user_cannot_view_another_users_profile(self):
        self.client.login(username='legituser', password='password')
        response = self.client.get('/ureporter/ffffffff-gggg-hhhh-iiii-jjjjjjjjjjjj/')
        self.assertEqual(response.status_code, 404)

    def test_user_can_view_own_profile(self):
        self.client.login(username='legituser', password='password')
        response = self.client.get('/ureporter/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee/')
        self.assertEqual(response.status_code, 200)
