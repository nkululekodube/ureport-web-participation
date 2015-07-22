from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^', views.rapidpro_receptor, name='rapidpro_receptor'),
]
