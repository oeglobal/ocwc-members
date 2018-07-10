from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.views.static import serve
from crm.views import IndexView, LoginKeyCheckView

admin.autodiscover()

urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/v1/', include('crm.urls_api', namespace='api', app_name='crm')),
    url(r'^crm/', include('crm.urls', namespace='crm', app_name='crm')),
    url(r'^staff/', include('crm.urls_staff', namespace='staff', app_name='crm')),
    url(r'^application/', include('crm.urls_application', namespace='application')),
    url(r'^comments/', include('djangospam.cookie.urls')),

    url(r'^login/(?P<key>[\w|\W]+)/$', LoginKeyCheckView.as_view(), name='login-key-check'),

    url(r'^conferences/', include('conferences.urls', namespace='conferences', app_name='conferences')),
    url(r'^elections/', include('elections.urls', namespace='elections', app_name='elections')),

    url(r'^tinymce/', include('tinymce.urls')),

    url(r'^$', IndexView.as_view(), name='crm_index'),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^theme/lib/(?P<path>.*)$', serve, {'document_root': '/Users/gandalf/hacking/mainsite/wp-content/themes/ocwc-mainsite/lib/'}),
        url(r'^theme/images/(?P<path>.*)$', serve, {'document_root': '/Users/gandalf/hacking/mainsite/wp-content/themes/ocwc-mainsite/images/'}),
        url(r'^media/logos/(?P<path>.*)$', serve, {'document_root': '/Users/gandalf/hacking/members/media/logos/'}),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
