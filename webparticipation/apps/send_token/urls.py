from django.conf.urls import url

from webparticipation.apps.send_token import views

urlpatterns = [
    url(r'^', views.send_token, name='send_token'),
]
