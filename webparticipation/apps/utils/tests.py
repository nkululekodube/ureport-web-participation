from django.test import TestCase
from views import dashify_user, undashify_user

class TestUtils(TestCase):


    def test_undashify_user(self):
        user = '4c21a87b-4031-4437-a4c5-afb5ddb42aad'
        undashified_user = undashify_user(user)
        self.assertEqual(undashified_user, '4c21a87b40314437a4c5afb5ddb42aad')


    def test_dashify_user(self):
        user = '4c21a87b40314437a4c5afb5ddb42aad'
        dashified_user = dashify_user(user)
        self.assertEqual(dashified_user, '4c21a87b-4031-4437-a4c5-afb5ddb42aad')
