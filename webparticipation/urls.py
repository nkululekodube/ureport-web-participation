from django.contrib import admin
from django.conf.urls import patterns, include, url

admin.autodiscover()

uuid_regex = '[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}'
password_reset_regex = '[\w\d]{32}'

urlpatterns = patterns(
    '',
    url(r'^$', include('apps.home.urls'), name='index'),
    url(r'^index/$', include('apps.home.urls'), name='home'),
    url(r'^register/$', include('apps.register.urls'), name='register'),
    url(r'^poll/', include('apps.poll_response.urls'), name='poll response'),
    url(r'^login/$', 'apps.ureport_auth.views.login_user', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^forgot-password/', 'apps.ureport_auth.views.forgot_password', name='forgot password'),
    url(r'^password-reset/(?P<reset_token>' + password_reset_regex + ')',
        'apps.ureport_auth.views.password_reset', name='reset password'),
    url(r'^ureporter/', include('apps.profile_page.urls'), name='profile'),
    url(r'^ureporter/(?P<ureporter_uuid>' + uuid_regex + ')/deactivate/$', include('apps.profile_page.urls'),
        name='profile'),
    url(r'^rapidpro-receptor', include('apps.rapidpro_receptor.urls'), name='rapidpro receptor'),
    url(r'^send-token', include('apps.send_token.urls'), name='send token'),
    url(r'^confirm-token', include('apps.confirm_token.urls'), name='confirm token'),
    url(r'^shout', include('apps.shout.urls')),
)
