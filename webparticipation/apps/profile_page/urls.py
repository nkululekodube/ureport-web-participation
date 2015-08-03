from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^', views.view_profile, name='profile page'),
    url(r'^/deactivate', views.deactivate_account, name='deactivate account'),
]
