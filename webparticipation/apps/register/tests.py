from django.test import TestCase, Client

class TestRegistration(TestCase):

    def test_registration_url_is_ok(self):
        response = self.client.get('/register/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'register.html')
