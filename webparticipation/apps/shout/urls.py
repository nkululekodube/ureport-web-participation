from django.conf.urls import url

from webparticipation.apps.shout.views import ShoutView

urlpatterns = [
    url(r'^', ShoutView.as_view(), name='shout'),
]
