from django.conf.urls import patterns, url

from .views import address_geo_list_view

urlpatterns = patterns('',
	url(r'^address/list/geo/$', address_geo_list_view, name='address-list-geo'),

)