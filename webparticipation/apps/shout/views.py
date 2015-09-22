from itertools import groupby

from braces.views import LoginRequiredMixin
from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.forms import Form
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.utils.translation import ugettext_lazy as _

from webparticipation.apps.rapidpro_receptor.views import send_message_to_rapidpro
from webparticipation.apps.ureporter.models import Ureporter
from webparticipation.api_client import get_runs_for_ureporter, get_poll_id




def validate_not_spaces(value):
    if value.strip() == '':
        raise ValidationError(_(u"Please enter a message."))


class ShoutForm(Form):
    message = forms.CharField(required=True, validators=[validate_not_spaces])


def user_in_flow(user):
    reporter = Ureporter.objects.get(user=user)
    data = get_runs_for_ureporter(reporter)
    in_flow = False
    flow_uuid = ''
    flows = {}
    for key, group in groupby(data.get('results'), lambda x: x.get('flow_uuid')):
        if any([item.get('completed') for item in group]):
            flows[key] = False
        else:
            flows[key] = True
    for key, value in flows.iteritems():
        if value:
            in_flow = True
            flow_uuid = key
            break
    return in_flow, flow_uuid


class ShoutView(LoginRequiredMixin, FormView):
    template_name = 'shout.html'
    form_class = ShoutForm
    success_url = '/shout'

    def get(self, request, *args, **kwargs):
        in_flow, flow_id = user_in_flow(request.user)
        form = self.get_form()
        context = self.get_context_data(form=form)
        if not in_flow:
            return self.render_to_response(context)
        else:
            poll_id = get_poll_id(flow_id)
            context['poll_id'] = poll_id
            has_poll = poll_id is not None
            context['has_poll'] = has_poll
            if has_poll:
                self.template_name = 'user_in_flow.html'
                messages.info(self.request, _('Please complete the poll before you can send us a message'))
            return self.render_to_response(context)

    def form_valid(self, form):
        reporter = Ureporter.objects.get(user=self.request.user)
        data = {'text': form.cleaned_data['message'], 'from': reporter.urn_tel}
        send_message_to_rapidpro(data)
        messages.info(self.request, _('Thank you change maker for sending U-Report this message'))
        return HttpResponseRedirect(self.get_success_url())
