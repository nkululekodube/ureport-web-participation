from django.conf.urls import url

from webparticipation.apps.profile_page import views

urlpatterns = [
    url(r'^$', views.view_profile, name='profile page'),
    url(r'^deactivate/?$', views.deactivate_account, name='deactivate account'),
    url(r'^goodbye/?$', views.goodbye, name='goodbye'),
    url(r'^unsubscribe/(?P<unsubscribe_token>[\d\w]{32})/?$', views.unsubscribe_account, name='unsubscribe'),
]
