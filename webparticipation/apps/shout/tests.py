from django.conf import settings

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django_webtest import WebTest
from mock import patch
import responses

from webparticipation.apps.shout.views import user_in_flow

from webparticipation.apps.ureporter.models import Ureporter


class ShoutViewTestCase(WebTest):
    url_name = "shout"

    def get_url(self):
        return reverse(self.url_name)

    def setUp(self):
        self.user = User.objects.create(username="mainuser", email="me@email.com")
        self.ureporter = Ureporter.objects.create(uuid="uuid", user=self.user, urn_tel="thecontact")

    @patch('webparticipation.apps.shout.views.user_in_flow')
    def test_requires_user_to_be_logged_in(self, mock_method):
        mock_method.return_value = False, ""
        response = self.app.get(self.get_url())
        self.assertRedirects(response, 'http://testserver/login/?next=/shout')

    @patch('webparticipation.apps.shout.views.user_in_flow')
    def test_correct_template_is_loaded(self, mock_method):
        mock_method.return_value = False, ""
        response = self.app.get(self.get_url(), user=self.user)
        self.assertTemplateUsed(response, 'shout.html')

    @patch('webparticipation.apps.shout.views.user_in_flow')
    def test_should_require_message(self, mock_method):
        mock_method.return_value = False, ""
        response = self.app.get(self.get_url(), user=self.user)
        form = response.form
        form['message'] = ''
        form_response = form.submit()
        self.assertEqual(form_response.context['form'].errors['message'][0], 'This field is required.')

    @patch('webparticipation.apps.shout.views.send_message_to_rapidpro')
    @patch('webparticipation.apps.shout.views.user_in_flow')
    def test_should_send_message_to_ureport_if_valid(self, mock_method, mock_send_to_rapidpro):
        mock_method.return_value = False, ""
        response = self.app.get(self.get_url(), user=self.user)
        form = response.form
        form['message'] = 'the world works'
        form.submit()
        mock_send_to_rapidpro.assert_called_with({'text': 'the world works', 'from': 'thecontact'})

    @patch('webparticipation.apps.shout.views.user_in_flow')
    def test_should_show_message_if_user_in_flow(self, mock_method):
        mock_method.return_value = True, "the poll flow uuid"
        response = self.app.get(self.get_url(), user=self.user)
        self.assertTemplateUsed(response, 'user_in_flow.html')


class TestUserInFlow(TestCase):
    username = "the wonder user"
    uuid = "the user man"

    def setUp(self):
        self.user = User.objects.create_user(username=self.username)
        self.ureporter = Ureporter.objects.create(uuid=self.uuid, user=self.user)
        self.ureporter.save()

    @responses.activate
    def test_user_not_in_flow_if_all_runs_completed(self):
        url = "%s/runs.json" % settings.RAPIDPRO_API_PATH
        responses.add(responses.GET, url,
                      body="""
                      {
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "flow_uuid": "05c66a1e-ff50-4b46-8739-8e7efeb699b0",
      "flow": 5,
      "run": 48,
      "completed": true
    },
    {
      "flow_uuid": "05c66a1e-ff50-4b46-8e7efeb699b0",
      "flow": 6,
      "run": 48,
      "completed": true
    }
  ]
}
                      """,
                      status=200,
                      content_type='application/json')
        self.assertEqual(False, user_in_flow(self.user)[0])

    @responses.activate
    def test_user_in_flow_if_any_runs_incomplete(self):
        url = "%s/runs.json" % settings.RAPIDPRO_API_PATH
        responses.add(responses.GET, url,
                      body="""
                      {
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "flow_uuid": "the-test-flow-uid",
      "flow": 5,
      "run": 48,
      "completed": false
    },
    {
      "flow_uuid": "05c66a1e-ff50-4b46-8e7efeb699b0",
      "flow": 6,
      "run": 48,
      "completed": true
    }
  ]
}
                      """,
                      status=200,
                      content_type='application/json')
        self.assertEqual(True, user_in_flow(self.user)[0])
        self.assertEqual('the-test-flow-uid', user_in_flow(self.user)[1])
