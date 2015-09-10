from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.test import RequestFactory
from django_webtest import WebTest


class ShoutViewTestCase(WebTest):
    url_name = "shout"

    def get_url(self):
        return reverse(self.url_name)

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="mainuser", email="me@email.com")

    def test_requires_user_to_be_logged_in(self):
        response = self.app.get(self.get_url())
        self.assertRedirects(response, 'http://testserver/login/?next=/shout')

    def test_correct_template_is_loaded(self):
        response = self.app.get(self.get_url(), user=self.user)
        self.assertTemplateUsed(response, 'shout.html')

    def test_should_require_message(self):
        response = self.app.get(self.get_url(), user=self.user)
        form = response.form
        form['message'] = ''
        form_response = form.submit()
        self.assertEqual(form_response.context['form'].errors['message'][0], 'This field is required.')
