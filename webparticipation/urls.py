from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^home/', TemplateView.as_view(template_name='base.html')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/', include('apps.register.urls')),
    url(r'^rapidpro-receptor', include('apps.rapidpro_receptor.urls')),
    url(r'^send-token', include('apps.send_token.urls')),
    url(r'^confirm-token', include('apps.confirm_token.urls')),
    url(r'^forgot-password/$', 'apps.login.views.forgot_password'),
    url(r'^login/$', 'apps.login.views.login_user'),
    url(r'^logout/$','django.contrib.auth.views.logout', {'next_page': '/'}),
)
