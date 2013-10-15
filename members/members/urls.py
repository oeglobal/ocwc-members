from django.conf.urls import patterns, include, url
from django.conf import settings

import djadmin2
djadmin2.default.autodiscover()

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'members.views.home', name='home'),
    # url(r'^members/', include('members.foo.urls')),

    url(r'^accounts/', include('django.contrib.auth.urls')),

   	url(r'^admin2/', include(djadmin2.default.urls)),
   	
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/v1/', include('crm.urls_api', namespace='api', app_name='crm')),
    url(r'^crm/', include('crm.urls', namespace='crm', app_name='crm')),
    url(r'^staff/', include('crm.urls_staff', namespace='staff', app_name='crm')),
    url(r'^application/', include('crm.urls_application', namespace='application')),

   	url(r'^$', 'crm.views.index', name='crm_index')
)

if settings.DEBUG:
	urlpatterns += patterns('',
		url(r'^theme/lib/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/gandalf/mainsite/wp-content/themes/ocwc-mainsite/lib/'}),
		url(r'^theme/images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/gandalf/mainsite/wp-content/themes/ocwc-mainsite/images/'}),
    url(r'^media/logos/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/gandalf/members/media/logos/'}),
	)