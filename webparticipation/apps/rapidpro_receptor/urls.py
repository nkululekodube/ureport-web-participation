from django.conf.urls import include, url
from . import views

urlpatterns = [
  url(r'^', views.rapidpro_receptor, name='rapidpro_receptor'),
]

