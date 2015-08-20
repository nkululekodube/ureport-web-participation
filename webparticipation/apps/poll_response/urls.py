from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<poll_id>[0-9]{1,6})/respond/', views.poll_response, name='poll response'),
    url(r'^latest/', views.latest_poll_response, name='latest poll response'),
]
