from django.conf.urls import patterns, url

from .views import OrganizationStaffListView

urlpatterns = patterns('',
    url(r'^organization/list/$', OrganizationStaffListView.as_view(), name='staff-organization-list'),

)
