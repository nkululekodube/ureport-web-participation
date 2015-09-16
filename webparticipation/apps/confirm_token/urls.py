from django.conf.urls import url

from webparticipation.apps.confirm_token import views

urlpatterns = [
    url(r'^', views.confirm_token, name='confirm_token'),
]
