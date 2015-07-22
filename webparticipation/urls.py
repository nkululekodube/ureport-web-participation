from django.contrib import admin
from django.conf.urls import patterns, include, url

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/', include('apps.register.urls')),
    url(r'^rapidpro-receptor', include('apps.rapidpro_receptor.urls')),
    url(r'^send-token', include('apps.send_token.urls')),
    url(r'^confirm-token', include('apps.confirm_token.urls')),
)
