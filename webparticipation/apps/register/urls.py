from django.conf.urls import url

from webparticipation.apps.register import views

urlpatterns = [
    url(r'^', views.register, name='register'),
]
