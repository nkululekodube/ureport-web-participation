from braces.views import LoginRequiredMixin
from django import forms
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.forms import Form
from django.http import HttpResponseRedirect
from django.views.generic import FormView
import requests

from webparticipation.apps.rapidpro_receptor.views import send_message_to_rapidpro

from webparticipation.apps.ureporter.models import Ureporter


def validate_not_spaces(value):
    if value.strip() == '':
        raise ValidationError(u"Please enter a message.")


class ShoutForm(Form):
    message = forms.CharField(required=True, validators=[validate_not_spaces])


def reduce_run(accumulator, item):
    if not item.get('completed'):
        accumulator[0] = True
        accumulator[1] = item.get('flow_uuid', '')
    return accumulator


def user_in_flow(user):
    reporter = Ureporter.objects.get(user=user)
    params = {'contact': reporter.uuid}
    headers = {'Authorization': 'Token %s' % settings.RAPIDPRO_API_TOKEN}
    url = '%s/runs.json' % settings.RAPIDPRO_API_PATH
    data = requests.get(url, params=params, headers=headers).json()
    return reduce(reduce_run, data['results'], [False, ''])


class ShoutView(LoginRequiredMixin, FormView):
    template_name = "shout.html"
    form_class = ShoutForm
    success_url = "/shout"

    def get(self, request, *args, **kwargs):
        in_flow, flow_id = user_in_flow(request.user)
        if not in_flow:
            form = self.get_form()
            return self.render_to_response(self.get_context_data(form=form))
        else:
            self.template_name = "user_in_flow.html"
            messages.info(self.request, 'Please complete the poll before you can send us a message')
            return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        reporter = Ureporter.objects.get(user=self.request.user)
        data = {'text': form.cleaned_data['message'], 'from': reporter.urn_tel}
        send_message_to_rapidpro(data)
        messages.info(self.request, 'Thank you change maker for sending ureport this message')
        return HttpResponseRedirect(self.get_success_url())
