from braces.views import LoginRequiredMixin
from django import forms
from django.core.exceptions import ValidationError
from django.forms import Form
from django.views.generic import FormView


def validate_not_spaces(value):
    if value.strip() == '':
        raise ValidationError(u"Please enter a message.")


class ShoutForm(Form):
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}),
                              validators=[validate_not_spaces])


class ShoutView(LoginRequiredMixin, FormView):
    template_name = "shout.html"
    form_class = ShoutForm
    success_url = "/shout"
