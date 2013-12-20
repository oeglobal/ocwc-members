from django.conf.urls import patterns, url

from .views import StaffIndex, OrganizationStaffView, OrganizationStaffListView, OrganizationStaffDetailView

# namespace='staff', app_name='crm'

urlpatterns = patterns('',
	url(r'^$', StaffIndex.as_view(), name='index'),

    url(r'^organization/view/(?P<pk>\d+)/$', OrganizationStaffDetailView.as_view(), name='organization-view'),
    url(r'^organization/list/$', OrganizationStaffListView.as_view(), name='organization-list'),
)
