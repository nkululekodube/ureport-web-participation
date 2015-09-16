from django.conf.urls import url

from webparticipation.apps.home import views

urlpatterns = [
    url(r'^', views.home, name='index'),
]
