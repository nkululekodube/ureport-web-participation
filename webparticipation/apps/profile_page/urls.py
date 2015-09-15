from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<ureporter_uuid>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})/$',
        views.view_profile, name='profile page'),
    url(r'^(?P<ureporter_uuid>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})/deactivate/$',
        views.deactivate_account, name='deactivate account'),
    url(r'^', views.unsubscribe_account, name='unsubscribe'),
]
