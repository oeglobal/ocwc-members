from django.conf.urls import patterns, include, url

import djadmin2
djadmin2.default.autodiscover()

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'members.views.home', name='home'),
    # url(r'^members/', include('members.foo.urls')),

   	url(r'^admin2/', include(djadmin2.default.urls)),
   	url(r'^admin/', include(admin.site.urls)),
)
