from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^', views.confirm_token, name='confirm_token'),
]
