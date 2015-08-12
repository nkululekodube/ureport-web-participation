from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^', views.poll_response, name='poll response'),
]
