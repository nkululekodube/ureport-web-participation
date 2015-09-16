from django.conf.urls import url

from webparticipation.apps.rapidpro_receptor import views

urlpatterns = [
    url(r'^', views.rapidpro_receptor, name='rapidpro_receptor'),
]
