from django.test import TestCase
from register.models import Registration

class TestRegistration(TestCase):

    def test_get_registration_is_ok(self):
        response = self.client.get('/register/')
        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'register.html')
