from django.test import TestCase
from models import generate_token, Ureporter
from django.contrib.auth.models import User


class TestUreporter(TestCase):

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

    def test_set_uuid(self):
        ureporter = Ureporter.objects.create(uuid='aaaaaaaa-bbbb-cccc-dddd-000000000000',
                                             user=User.objects.create_user('changeMyUuid'))
        self.assertEqual(ureporter.uuid, 'aaaaaaaa-bbbb-cccc-dddd-000000000000')
        ureporter.set_uuid('aaaaaaaa-bbbb-cccc-dddd-111111111111')
        self.assertNotEqual(ureporter.uuid, 'aaaaaaaa-bbbb-cccc-dddd-000000000000')
        self.assertEqual(ureporter.uuid, 'aaaaaaaa-bbbb-cccc-dddd-111111111111')

    # def test_token_has_expired(self):
    #     ureporter = Ureporter.objects.create(uuid='aaaaaaaa-bbbb-cccc-dddd-000000000000',
    #                                          user=User.objects.create_user('newUser'))
    #     expired = ureporter.token_has_expired()
    #     self.assertEqual(expired, False)

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

    def test_delete_user(self):
        ureporter = Ureporter.objects.create(uuid='aaaaaaaa-bbbb-cccc-dddd-zzzzzzzzzzzz',
                                             user=User.objects.create_user('deleteMe'))
        self.assertEqual(User.objects.filter(username='deleteMe').exists(), True)
        self.assertEqual(Ureporter.objects.filter(uuid='aaaaaaaa-bbbb-cccc-dddd-zzzzzzzzzzzz').exists(), True)
        ureporter.delete()
        self.assertEqual(User.objects.filter(username='deleteMe').exists(), False)
        self.assertEqual(Ureporter.objects.filter(uuid='aaaaaaaa-bbbb-cccc-dddd-zzzzzzzzzzzz').exists(), False)
