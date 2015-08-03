from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^home/', TemplateView.as_view(template_name='base.html'), name='home'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls'), name='docs'),
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^register/', include('apps.register.urls'), name='register'),
    url(r'^rapidpro-receptor', include('apps.rapidpro_receptor.urls'), name='rapidpro receptor'),
    url(r'^send-token', include('apps.send_token.urls'), name='send token'),
    url(r'^confirm-token', include('apps.confirm_token.urls'), name='confirm token'),
    url(r'^forgot-password/$', 'apps.login.views.forgot_password', name='forgot password'),
    url(r'^login/$', 'apps.login.views.login_user', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^ureporter/(?P<ureporter_uuid>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})/$',
        include('apps.profile_page.urls'), name='profile'),
    url(r'^ureporter/(?P<ureporter_uuid>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})/deactivate/$',
        include('apps.profile_page.urls'), name='profile'),

)
