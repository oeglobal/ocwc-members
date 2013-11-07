from django.conf.urls import patterns, url

from .views import address_geo_list_view, country_list_view, OrganizationByCountryListViewApi, \
				   organization_group_by_membership_view, OrganizationViewApi

urlpatterns = patterns('',
	url(r'^address/list/geo/$', address_geo_list_view, name='address-list-geo'),
	url(r'^country/list/$', country_list_view, name='country-list'),
	url(r'^organization/view/(?P<pk>\d+)/$', OrganizationViewApi.as_view(), name='organization-view'),
	url(r'^organization/by_country/(?P<country>[\w|\W]+)/list/$', OrganizationByCountryListViewApi.as_view(lookup_field='country'), name='organization-by_country-list'),
	url(r'^organization/group_by/membership_type/list/$', organization_group_by_membership_view, name='organization-group_by_membership_type-list' ),
)